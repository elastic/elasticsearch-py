from multiprocessing.dummy import Pool

from . import _process_bulk_chunk, _chunk_actions, expand_action


def parallel_bulk(client, actions, thread_count=4, chunk_size=500,
        max_chunk_bytes=100 * 1014 * 1024,
        expand_action_callback=expand_action, **kwargs):
    """
    Parallel version of the bulk helper.
    """
    actions = map(expand_action_callback, actions)

    pool = Pool(thread_count)

    for result in pool.imap(
        lambda chunk: list(_process_bulk_chunk(client, chunk, **kwargs)),
        _chunk_actions(actions, chunk_size, max_chunk_bytes, client.transport.serializer)
        ):
        for item in result:
            yield item

    pool.close()
    pool.join()
