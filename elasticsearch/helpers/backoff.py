import time

from . import expand_action, _chunk_actions, _process_bulk_chunk
from ..exceptions import TransportError


def backoff_bulk(client, actions, chunk_size=500, max_chunk_bytes=100 * 1024 * 1024,
                 expand_action_callback=expand_action, max_retries=-1,
                 initial_backoff=2, max_backoff=600, **kwargs):
    """
    Bulk helper that implements proper retry strategy when dealing with
    rejecttions - when the target cluster is overloaded, returning ``429``
    responses, the bulk actions will be retried after a backoff period to allow
    the cluster to recover.

    This function is a generator yielding all documents that failed to index.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use
    :arg actions: iterable containing the actions to be executed
    :arg chunk_size: number of docs in one chunk sent to es (default: 500)
    :arg max_chunk_bytes: the maximum size of the request in bytes (default: 100MB)
    :arg expand_action_callback: callback executed on each action passed in,
        should return a tuple containing the action line and the data line
        (`None` if data line should be omitted).
    :arg max_retries: maximum number of times a document will be retried
    :arg initial_backoff: number of seconds we should wait before the first
        retry. Any subsequent retries will be powers of ``inittial_backoff *
        2**retry_number``
    :arg max_backoff: maximum number of seconds a retry will wait
    """
    actions = map(expand_action_callback, actions)

    for bulk_data, bulk_actions in _chunk_actions(actions, chunk_size,
                                                  max_chunk_bytes,
                                                  client.transport.serializer):
        retry = 0
        while max_retries == -1 or retry <= max_retries:
            to_retry, to_retry_data = [], []
            if retry:
                time.sleep(min(max_backoff, initial_backoff * 2**(retry-1)))

            try:
                for data, (ok, info) in zip(bulk_data,
                                            _process_bulk_chunk(client,
                                                                bulk_actions,
                                                                bulk_data,
                                                                raise_on_exception=True,
                                                                raise_on_error=False,
                                                                **kwargs)):

                    if not ok:
                        action, info = info.popitem()
                        if info['status'] == 429 and (retry+1) <= max_retries:
                            to_retry.extend(data)
                            to_retry_data.append(data)
                        else:
                            info['data'] = data
                            yield {action: info}

            except TransportError as e:
                if e.status_code != 429:
                    raise
                retry += 1
            else:
                if not to_retry:
                    break
                bulk_actions = to_retry
                bulk_data = to_retry_data

                retry += 1
