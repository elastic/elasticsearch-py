from itertools import islice
from operator import methodcaller

from ..exceptions import ElasticsearchException
from ..compat import map

class BulkIndexError(ElasticsearchException):
    @property
    def errors(self):
        """ List of errors from execution of the last chunk. """
        return self.args[1]


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


def streaming_bulk(client, actions, chunk_size=500, raise_on_error=False, expand_action_callback=expand_action, **kwargs):
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

    Alternative actions (`_op_type` field defaults to `index`) can be sent as
    well::

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
    :arg raise_on_error: raise `BulkIndexError` containing errors (as `.errors`
        from the execution of the last chunk)
    :arg expand_action_callback: callback executed on each action passed in,
        should return a tuple containing the action line and the data line
        (`None` if data line should be omitted).
    """
    actions = map(expand_action_callback, actions)

    # if raise on error is set, we need to collect errors per chunk before raising them
    errors = []

    while True:
        chunk = islice(actions, chunk_size)
        bulk_actions = []
        for action, data in chunk:
            bulk_actions.append(action)
            if data is not None:
                bulk_actions.append(data)

        if not bulk_actions:
            return

        # send the actual request
        resp = client.bulk(bulk_actions, **kwargs)

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

def scan(client, query=None, scroll='5m', **kwargs):
    """
    Simple abstraction on top of the
    :meth:`~elasticsearch.Elasticsearch.scroll` api - a simple iterator that
    yields all hits as returned by underlining scroll requests.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use
    :arg query: body for the :meth:`~elasticsearch.Elasticsearch.search` api
    :arg scroll: Specify how long a consistent view of the index should be
        maintained for scrolled search

    Any additional keyword arguments will be passed to the initial
    :meth:`~elasticsearch.Elasticsearch.search` call.
    """
    # initial search to
    resp = client.search(body=query, search_type='scan', scroll=scroll, **kwargs)

    scroll_id = resp['_scroll_id']

    while True:
        resp = client.scroll(scroll_id, scroll=scroll)
        if not resp['hits']['hits']:
            break
        for hit in resp['hits']['hits']:
            yield hit
        scroll_id = resp['_scroll_id']

def reindex(client, source_index, target_index, target_client=None, chunk_size=500, scroll='5m'):
    """
    Reindex all documents from one index to another, potentially (if
    `target_client` is specified) on a different cluster.

    .. note::

        This helper doesn't transfer mappings, just the data.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use (for
        read if `target_client` is specified as well)
    :arg source_index: index (or list of indices) to read documents from
    :arg target_index: name of the index in the target cluster to populate
    :arg target_client: optional, is specified will be used for writing (thus
        enabling reindex between clusters)
    :arg chunk_size: number of docs in one chunk sent to es (default: 500)
    :arg scroll: Specify how long a consistent view of the index should be
        maintained for scrolled search
    """
    target_client = client if target_client is None else target_client

    docs = scan(client, index=source_index, scroll=scroll)
    def _change_doc_index(hits, index):
        for h in hits:
            h['_index'] = index
            yield h

    return bulk(target_client, _change_doc_index(docs, target_index),
        chunk_size=chunk_size, stats_only=True)
