import numpy as np
import tensorflow as tf
import torch

import functools
import time

def print_dict(input_dict, only_keys=False, type_for_print=None, recursive_dict=True, recursive_list=True, prefix=''):
    type_for_print = type_for_print or [int, float, str, list, bool, np.bool_, np.uint8]
    print(type(input_dict))

    if isinstance(input_dict, dict):
        if only_keys:
            for k, v in input_dict.items():
                if isinstance(v, dict) and recursive_dict:
                    print(prefix + str(k) + str(type(v)) + ':')
                    print_dict(v, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix + '\t')
                else:
                    print(prefix + str(k))
        else:
            for k, v in input_dict.items():
                if isinstance(v, dict) and recursive_dict:
                    print(prefix + str(k) + str(type(v)) + ':')
                    print_dict(v, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix + '\t')
                elif isinstance(v, np.ndarray):
                    if type(v) in type_for_print:
                        print(prefix + "{}: {}, {}, {}".format(k, type(v), v.shape, v))
                    else:
                        print(prefix + "{}: {}, {}".format(k, type(v), v.shape))
                elif isinstance(v, list) and list in type_for_print and recursive_list:
                    print(prefix + str(k) + str(type(v)) + ':')
                    for list_v in v:
                        if isinstance(list_v, dict):
                            print_dict(list_v, only_keys, type_for_print, recursive_dict, recursive_list,
                                       prefix=prefix + '\t')
                        else:
                            if type(list_v) in type_for_print:
                                print(prefix + '\t' + "{}, {}".format(type(list_v), list_v))
                            else:
                                print(prefix + '\t' + "{}".format(type(list_v)))
                else:
                    if type(v) in type_for_print:
                        print(prefix + "{}: {}, {}".format(k, type(v), v))
                    else:
                        print(prefix + "{}: {}".format(k, type(v)))
    elif isinstance(input_dict, list):
        for item in input_dict:
            print_dict(item, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix)
            print("------------------")
    else:
        print(prefix + '\t' + str(type(input_dict)))

    print()


def timer(func):
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


data = {"1_1": {"1_1_1": "vege", "1_1_2": "nana"}, "1_2": "semmi", "1_3": {"1_3_1": {"1_3_1_1": "juhu", "1_3_1_2": "wao"}, "1_3_2": "a-a"}}


if __name__ == "__main__":
	print_dict(data, only_keys=False, type_for_print=[str, float, int, list], recursive_dict=True)
