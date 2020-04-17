import functools
import time

def jtimer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

def make_index_chunks(indexes, pool_size):
    len_of_chunk = im_width // pool_size
    chunks = [indexes[x:x + len_of_chunk] for x in range(0, len(indexes), len_of_chunk)]
    return chunks


def new_thread(func):
    """Start a new thread for the function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        x = threading.Thread(target=func, args=args, kwargs=kwargs)
        x.start()
    return wrapper_timer

