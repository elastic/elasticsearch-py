from itertools import islice

def bulk_index(client, docs, chunk_size=500, **kwargs):
    """
    Helper for the :meth:`~elasticsearch.Elasticsearch.bulk` api that provides
    a more human friendly interface - it consumes an iterator of documents and
    sends them to elasticsearch in chunks.

    This function expects the doc to be in the format as returned by
    :meth:`~elasticsearch.Elasticsearch.search`, for example::

        {
            '_index': 'index-name',
            '_type': 'document',
            '_parent': '5',
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

    Any additional keyword arguments will be passed to the bulk API itself.
    """
    success, failed = [], []
    docs = iter(docs)
    while True:
        chunk = islice(docs, chunk_size)
        bulk_actions = []
        for d in chunk:
            action = {'index': {}}
            for key in ('_index', '_parent', '_percolate', '_routing',
                        '_timestamp', '_ttl', '_type', '_version',):
                if key in d:
                    action['index'][key] = d.pop(key)

            bulk_actions.append(action)
            bulk_actions.append(d.get('_source', d))

        if not bulk_actions:
            return success, failed

        resp = client.bulk(bulk_actions, **kwargs)

        for item in resp['items']:
            if item['create']['ok']:
                success.append(item)
            else:
                failed.append(item)

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

    return bulk_index(target_client, _change_doc_index(docs, target_index), chunk_size=chunk_size)
