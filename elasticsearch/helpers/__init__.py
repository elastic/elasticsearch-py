import logging
from itertools import islice
from operator import methodcaller

from ..exceptions import ElasticsearchException, TransportError
from ..compat import map

logger = logging.getLogger('elasticsearch.helpers')

class BulkIndexError(ElasticsearchException):
    @property
    def errors(self):
        """ List of errors from execution of the last chunk. """
        return self.args[1]


class ScanError(ElasticsearchException):
    pass

def expand_action(data):
    """
    From one document or action definition passed in by the user extract the
    action/data lines needed for elasticsearch's
    :meth:`~elasticsearch.Elasticsearch.bulk` api.
    """
    # make sure we don't alter the action
    data = data.copy()
    op_type = data.pop('_op_type', 'index')
    action = {op_type: {}}
    for key in ('_index', '_parent', '_percolate', '_routing', '_timestamp',
            '_ttl', '_type', '_version', '_version_type', '_id', '_retry_on_conflict'):
        if key in data:
            action[op_type][key] = data.pop(key)

    # no data payload for delete
    if op_type == 'delete':
        return action, None

    return action, data.get('_source', data)

def _chunk_actions(actions, chunk_size):
    while True:
        yield islice(actions, chunk_size)

def streaming_bulk(client, actions, chunk_size=500, raise_on_error=True,
        expand_action_callback=expand_action, raise_on_exception=True, 
        **kwargs):
    """
    Streaming bulk consumes actions from the iterable passed in and yields
    results per action. For non-streaming usecases use
    :func:`~elasticsearch.helpers.bulk` which is a wrapper around streaming
    bulk that returns summary information about the bulk operation once the
    entire input is consumed and sent.

    This function expects the action to be in the format as returned by
    :meth:`~elasticsearch.Elasticsearch.search`, for example::

        {
            '_index': 'index-name',
            '_type': 'document',
            '_id': 42,
            '_parent': 5,
            '_ttl': '1d',
            '_source': {
                ...
            }
        }

    Alternatively, if `_source` is not present, it will pop all metadata fields
    from the doc and use the rest as the document data.

    The :meth:`~elasticsearch.Elasticsearch.bulk` api accepts `index`, `create`,
    `delete`, and `update` actions. Use the `_op_type` field to specify an
    action (`_op_type` defaults to `index`)::

        {
            '_op_type': 'delete',
            '_index': 'index-name',
            '_type': 'document',
            '_id': 42,
        }
        {
            '_op_type': 'update',
            '_index': 'index-name',
            '_type': 'document',
            '_id': 42,
            'doc': {'question': 'The life, universe and everything.'}
        }

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use
    :arg actions: iterable containing the actions to be executed
    :arg chunk_size: number of docs in one chunk sent to es (default: 500)
    :arg raise_on_error: raise ``BulkIndexError`` containing errors (as `.errors`)
        from the execution of the last chunk when some occur. By default we raise.
    :arg raise_on_exception: if ``False`` then don't propagate exceptions from
        call to ``bulk`` and just report the items that failed as failed.
    :arg expand_action_callback: callback executed on each action passed in,
        should return a tuple containing the action line and the data line
        (`None` if data line should be omitted).
    """
    actions = map(expand_action_callback, actions)

    # if raise on error is set, we need to collect errors per chunk before raising them
    errors = []

    for chunk in _chunk_actions(actions, chunk_size):

        bulk_actions = []
        for action, data in chunk:
            bulk_actions.append(action)
            if data is not None:
                bulk_actions.append(data)

        if not bulk_actions:
            return

        try:
            # send the actual request
            resp = client.bulk(bulk_actions, **kwargs)
        except TransportError as e:
            # default behavior - just propagate exception
            if raise_on_exception:
                raise e

            # if we are not propagating, mark all actions in current chunk as failed
            err_message = str(e)
            exc_errors = []
            bulk_data = iter(bulk_actions)
            while True:
                try:
                    # collect all the information about failed actions
                    action = next(bulk_data)
                    op_type, action = action.popitem()
                    info = {"error": err_message, "status": e.status_code, "exception": e}
                    if op_type != 'delete':
                        info['data'] = next(bulk_data)
                    info.update(action)
                    exc_errors.append({op_type: info})
                except StopIteration:
                    break

            # emulate standard behavior for failed actions
            if raise_on_error:
                raise BulkIndexError('%i document(s) failed to index.' % len(exc_errors), exc_errors)
            else:
                for err in exc_errors:
                    yield False, err
                continue

        # go through request-reponse pairs and detect failures
        for op_type, item in map(methodcaller('popitem'), resp['items']):
            ok = 200 <= item.get('status', 500) < 300
            if not ok and raise_on_error:
                errors.append({op_type: item})

            if not errors:
                # if we are not just recording all errors to be able to raise
                # them all at once, yield items individually
                yield ok, {op_type: item}

        if errors:
            raise BulkIndexError('%i document(s) failed to index.' % len(errors), errors)

def bulk(client, actions, stats_only=False, **kwargs):
    """
    Helper for the :meth:`~elasticsearch.Elasticsearch.bulk` api that provides
    a more human friendly interface - it consumes an iterator of actions and
    sends them to elasticsearch in chunks. It returns a tuple with summary
    information - number of successfully executed actions and either list of
    errors or number of errors if `stats_only` is set to `True`.

    See :func:`~elasticsearch.helpers.streaming_bulk` for more information
    and accepted formats.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use
    :arg actions: iterator containing the actions
    :arg stats_only: if `True` only report number of successful/failed
        operations instead of just number of successful and a list of error responses

    Any additional keyword arguments will be passed to
    :func:`~elasticsearch.helpers.streaming_bulk` which is used to execute
    the operation.
    """
    success, failed = 0, 0

    # list of errors to be collected is not stats_only
    errors = []

    for ok, item in streaming_bulk(client, actions, **kwargs):
        # go through request-reponse pairs and detect failures
        if not ok:
            if not stats_only:
                errors.append(item)
            failed += 1
        else:
            success += 1

    return success, failed if stats_only else errors

# preserve the name for backwards compatibility
bulk_index = bulk

def scan(client, query=None, scroll='5m', raise_on_error=True, preserve_order=False, **kwargs):
    """
    Simple abstraction on top of the
    :meth:`~elasticsearch.Elasticsearch.scroll` api - a simple iterator that
    yields all hits as returned by underlining scroll requests.

    By default scan does not return results in any pre-determined order. To
    have a standard order in the returned documents (either by score or
    explicit sort definition) when scrolling, use ``preserve_order=True``. This
    may be an expensive operation and will negate the performance benefits of
    using ``scan``.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use
    :arg query: body for the :meth:`~elasticsearch.Elasticsearch.search` api
    :arg scroll: Specify how long a consistent view of the index should be
        maintained for scrolled search
    :arg raise_on_error: raises an exception (``ScanError``) if an error is
        encountered (some shards fail to execute). By default we raise.
    :arg preserve_order: don't set the ``search_type`` to ``scan`` - this will
        cause the scroll to paginate with preserving the order. Note that this
        can be an extremely expensive operation and can easily lead to
        unpredictable results, use with caution.

    Any additional keyword arguments will be passed to the initial
    :meth:`~elasticsearch.Elasticsearch.search` call::

        scan(es,
            query={"match": {"title": "python"}},
            index="orders-*",
            doc_type="books"
        )

    """
    if not preserve_order:
        kwargs['search_type'] = 'scan'
    # initial search
    resp = client.search(body=query, scroll=scroll, **kwargs)

    scroll_id = resp.get('_scroll_id')
    if scroll_id is None:
        return

    first_run = True
    while True:
        # if we didn't set search_type to scan initial search contains data
        if preserve_order and first_run:
            first_run = False
        else:
            resp = client.scroll(scroll_id, scroll=scroll)

        for hit in resp['hits']['hits']:
            yield hit

        # check if we have any errrors
        if resp["_shards"]["failed"]:
            logger.warning(
                'Scrol request has failed on %d shards out of %d.',
                resp['_shards']['failed'], resp['_shards']['total']
            )
            if raise_on_error:
                raise ScanError(
                    'Scrol request has failed on %d shards out of %d.',
                    resp['_shards']['failed'], resp['_shards']['total']
                )

        scroll_id = resp.get('_scroll_id')
        # end of scroll
        if scroll_id is None or not resp['hits']['hits']:
            break

def reindex(client, source_index, target_index, query=None, target_client=None,
        chunk_size=500, scroll='5m', scan_kwargs={}, bulk_kwargs={}):

    """
    Reindex all documents from one index that satisfy a given query
    to another, potentially (if `target_client` is specified) on a different cluster.
    If you don't specify the query you will reindex all the documents.

    .. note::

        This helper doesn't transfer mappings, just the data.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use (for
        read if `target_client` is specified as well)
    :arg source_index: index (or list of indices) to read documents from
    :arg target_index: name of the index in the target cluster to populate
    :arg query: body for the :meth:`~elasticsearch.Elasticsearch.search` api
    :arg target_client: optional, is specified will be used for writing (thus
        enabling reindex between clusters)
    :arg chunk_size: number of docs in one chunk sent to es (default: 500)
    :arg scroll: Specify how long a consistent view of the index should be
        maintained for scrolled search
    :arg scan_kwargs: additional kwargs to be passed to
        :func:`~elasticsearch.helpers.scan`
    :arg bulk_kwargs: additional kwargs to be passed to
        :func:`~elasticsearch.helpers.bulk`
    """
    target_client = client if target_client is None else target_client

    docs = scan(client,
        query=query,
        index=source_index,
        scroll=scroll,
        fields=('_source', '_parent', '_routing', '_timestamp'),
        **scan_kwargs
    )
    def _change_doc_index(hits, index):
        for h in hits:
            h['_index'] = index
            if 'fields' in h:
                h.update(h.pop('fields'))
            yield h

    kwargs = {
        'stats_only': True,
    }
    kwargs.update(bulk_kwargs)
    return bulk(target_client, _change_doc_index(docs, target_index),
        chunk_size=chunk_size, **kwargs)
