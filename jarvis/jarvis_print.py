import numpy as np
import tensorflow as tf
import torch

def jprint(input_dict, only_keys=False, type_for_print=None, recursive_dict=True, recursive_list=True, prefix=''):
    type_for_print = type_for_print or [int, float, str, list, bool, np.bool_, np.uint8]
    # print(prefix + str(type(input_dict)))

    if isinstance(input_dict, dict):
        if only_keys:
            for k, v in input_dict.items():
                if isinstance(v, dict) and recursive_dict:
                    print(prefix + str(k) + str(type(v)) + ':')
                    jprint(v, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix + '\t')
                else:
                    print(prefix + str(k) + str(type(v)))
        else:
            for k, v in input_dict.items():
                if isinstance(v, dict) and recursive_dict:
                    print(prefix + str(k) + str(type(v)) + ':')
                    jprint(v, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix + '\t')
                elif isinstance(v, np.ndarray):
                    if type(v) in type_for_print:
                        print(prefix + "{}: {}, {}, {}".format(k, type(v), v.shape, v))
                    else:
                        print(prefix + "{}: {}, {}".format(k, type(v), v.shape))
                elif isinstance(v, list) and list in type_for_print and recursive_list:
                    print(prefix + str(k) + str(type(v)) + ':')
                    for list_v in v:
                        if isinstance(list_v, dict):
                            jprint(list_v, only_keys, type_for_print, recursive_dict, recursive_list,
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
            jprint(item, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix + '\t')
            print("------------------")
    else:
        print(prefix + '\t' + str(type(input_dict)))

    print()
