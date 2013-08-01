from itertools import islice

def bulk_index(client, docs, chunk_size=500, **kwargs):
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
    target_client = client if target_client is None else target_index

    docs = scan(client, index=source_index, scroll=scroll)
    def _change_doc_index(hits, index):
        for h in hits:
            h['_index'] = index
            yield h

    return bulk_index(target_client, _change_doc_index(docs, target_index), chunk_size=chunk_size)
