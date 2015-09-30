from multiprocessing.dummy import Pool
from queue import Empty, Queue

from threading import Event

from . import streaming_bulk

def consume(queue, done):
    """
    Create an iterator on top of a Queue.
    """
    while True:
        try:
            yield queue.get(True, .01)
        except Empty:
            if done.is_set():
                break

def wrapped_bulk(client, input, output, done, **kwargs):
    """
    Wrap a call to streaming_bulk by feeding it data frm a queue and writing
    the outputs to another queue.
    """
    try:
        for result in streaming_bulk(client, consume(input, done), **kwargs):
            output.put(result)
    except:
        done.set()
        raise

def feed_data(actions, input, done):
    """
    Feed data from an iterator into a queue.
    """
    for a in actions:
        input.put(a, True)

        # error short-circuit
        if done.is_set():
            break
    done.set()


def parallel_bulk(client, actions, thread_count=5, **kwargs):
    """
    Paralel version of the bulk helper. It runs a thread pool with a thread for
    a producer and ``thread_count`` threads for.
    """
    done = Event()
    input, output = Queue(), Queue()
    pool = Pool(thread_count + 1)

    results = [
        pool.apply_async(wrapped_bulk, (client, input, output, done), kwargs)
        for _ in range(thread_count)]
    pool.apply_async(feed_data, (actions, input, done))

    while True:
        try:
            yield output.get(True, .01)
        except Empty:
            if done.is_set() and all(r.ready() for r in results):
                break

    pool.close()
    pool.join()
