import pickle
import os
import functools
from termcolor import colored


def load_cache(cache_path):
    print(colored("Use cache", color="green") + " with path: " + cache_path + '\n')

    loaded_object = None
    try:
        with open(cache_path, 'rb') as cache_file:
            loaded_object = pickle.load(cache_file)
    except Exception as e:
        print(e)
        print(colored("Cache loading is unsuccessful!", color="red") + '\n')

    return loaded_object


def save_cache(object_to_save, cache_path):
    try:
        with open(cache_path, 'wb') as cache_file:
            pickle.dump(object_to_save, cache_file)

        print(colored("Cache saving is successful", color="green") + " with path: " + cache_path + '\n')
    except Exception as e:
        print(e)
        print(colored("Cache saving is unsuccessful!", color="red") + '\n')


def cache(func):
    @functools.wraps(func)
    def cache_wrapper(*args, **kwargs):
        use_cache = kwargs["use_cache"]
        cache_loaded = False
        return_object = None
        cache_path = None

        if use_cache:
            if len(args) > 0:
                path = args[0]
            else:
                for key in kwargs.keys():
                    if key.find("path") != -1:
                        path = kwargs[key]
            cache_path = "cache/" + "".join(os.path.splitext(path)[0].split('/')) + ".pkl"
            return_object = load_cache(cache_path)

            if return_object is not None:
                cache_loaded = True

        if not cache_loaded:
            return_object = func(*args, **kwargs)

            if use_cache:
                save_cache(return_object, cache_path)

        return return_object

    return cache_wrapper
