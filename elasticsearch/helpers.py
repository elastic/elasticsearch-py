from itertools import islice

from elasticsearch.exceptions import ElasticsearchException

class BulkIndexError(ElasticsearchException): pass

def bulk_index(client, docs, chunk_size=500, stats_only=False, raise_on_error=False, **kwargs):
    """
    Helper for the :meth:`~elasticsearch.Elasticsearch.bulk` api that provides
    a more human friendly interface - it consumes an iterator of documents and
    sends them to elasticsearch in chunks.

    This function expects the doc to be in the format as returned by
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

    alternatively, if `_source` is not present, it will pop all metadata fields
    from the doc and use the rest as the document data.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use
    :arg docs: iterator containing the docs
    :arg chunk_size: number of docs in one chunk sent to es (default: 500)
    :arg stats_only: if `True` only report number of successful/failed
        operations instead of just number of successful and a list of error responses
    :arg raise_on_error: raise `BulkIndexError` if some documents failed to
        index (and stop sending chunks to the server)

    Any additional keyword arguments will be passed to the bulk API itself.
    """
    success, failed = 0, 0

    # list of errors to be collected when 
    errors = []

    docs = iter(docs)
    while True:
        chunk = islice(docs, chunk_size)
        bulk_actions = []
        for d in chunk:
            action = {'index': {}}
            for key in ('_index', '_parent', '_percolate', '_routing',
                        '_timestamp', '_ttl', '_type', '_version', '_id'):
                if key in d:
                    action['index'][key] = d.pop(key)

            bulk_actions.append(action)
            bulk_actions.append(d.get('_source', d))

        if not bulk_actions:
            return success, failed if stats_only else errors

        # send the actual request
        resp = client.bulk(bulk_actions, **kwargs)

        # go through request-reponse pairs and detect failures
        for req, item in zip(bulk_actions[::2], resp['items']):
            ok = item['index' if '_id' in req['index'] else 'create'].get('ok')
            if not ok:
                if not stats_only:
                    errors.append(item)
                failed += 1
            else:
                success += 1

        if failed and raise_on_error:
            raise BulkIndexError('%i document(s) failed to index.' % failed, errors)


class BulkCommand(object):
    """A command to be supplied to the :meth:`~elasticsearch.helpers.streaming_bulk_index` interface.

    This is a convenience class which allows external data to be associated
    with bulk commands; the external data isn't sent to elasticsearch but will
    be available when processing the results of
    :meth:`~elasticsearch.helpers.streaming_bulk_index`.  For example, if you
    were reading data to send to elasticsearch from a persistent queue, you
    could use this external data to hold a message ID, and wait for
    elasticsearches response to ack or nack the message appropriately.

    """
    def __init__(self, action, source=None, ext=None):
        """
        :arg action: A dict containing the action part of the command to send.
        :arg source: A dict containing the source part of the command; use this
            for commands which require a source.
        :arg ext: Arbitrary external data; this will not be sent to
            elasticsearch.

        """
        self.cmds = [action]
        if source is not None:
            self.cmds.append(source)
        self.ext = ext

    def __getitem__(self, index):
        return self.cmds[index]


def streaming_bulk_index(client, bulk_commands, chunk_size=500, **kwargs):
    """Perform a bulk update in a streaming manner.

    This accepts a stream of commands and yields a stream of results of sending
    the commands to elasticsearch.  The commands are performed in chunks, sized
    according to the `chunk_size` parameter.  Unlike the bulk_index method,
    this isn't limited to the `index` action, and doesn't require all the
    updates to be performed before the results of the updates are reported.

    The commands should be exactly the structures to be sent to elasticsearch,
    as 1-or-2 length sequence objects (ie, sequences of [action_and_meta_data]
    or [action_and_meta_data, optional_source]), for example bulk_commands
    could be a list containing::

        [
            [
                {"index": {"_index": "test", "_type": "type1", "_id": "1"}},
                {"field1": "value1"},
            ],
            [
                {"delete": {"_index": "test", "_type": "type1", "_id": "2"}},
            ],
        ]

    The :class:`~elasticsearch.helpers.BulkCommand` class can also be used to
    represent commands in `bulk_commands`.  This is particularly useful if you
    want to associate some external data with the commands to assist with
    handling failures.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use.

    :arg bulk_commands: a sequence or iterable of commands.  Each command
        is a 1-or-2 length list containing the command, and the
        document data associated with the command (if the command expects such
        data).

    :arg chunk_size: the number of commands to send to elasticsearch at
        once.

    Any additional keyword arguments will be passed to the bulk API itself.

    This yields a sequence of (`ok`, `cmd`, `cmd_result`) items, one for each
    command in `bulk_commands`, where `ok` is `True` if the command was
    processed without error, and `False` otherwise, `cmd` is the original
    command read from `bulk_commands`, and `cmd_result` is the response for
    that command received from the server.

    """
    bulk_commands = iter(bulk_commands)
    while True:
        chunk = tuple(islice(bulk_commands, chunk_size))
        if len(chunk) == 0:
            break

        # Flatten the commands into a single list to send to the server
        cmds = []
        for cmd in chunk:
            cmds.extend(cmd)

        # Send the commands, and then iterate through the response to yield the
        # results
        result = client.bulk(body=cmds, **kwargs)
        assert len(result['items']) == len(chunk)
        for cmd, cmd_result in zip(chunk, result['items']):
            assert len(cmd_result) == 1
            ok = bool(tuple(cmd_result.values())[0].get('ok'))
            yield ok, cmd, cmd_result


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
    target_client = client if target_client is None else target_index

    docs = scan(client, index=source_index, scroll=scroll)
    def _change_doc_index(hits, index):
        for h in hits:
            h['_index'] = index
            yield h

    return bulk_index(target_client, _change_doc_index(docs, target_index),
        chunk_size=chunk_size, stats_only=True)
