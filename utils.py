import numpy as np
import tensorflow as tf
import torch

def print_dict(input_dict, only_keys=False, type_for_print=None, recursive_dict=True, recursive_list=False, prefix=''):
    type_for_print = type_for_print or [int, float]

    if only_keys:
        for k, v in input_dict.items():
            if isinstance(v, dict) and recursive_dict:
                print(prefix + k + str(type(v)) + ':')
                print_dict(v, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix + '\t')
            else:
                print(prefix + k)
    else:
        for k, v in input_dict.items():
            if isinstance(v, dict) and recursive_dict:
                print(prefix + k + str(type(v)) + ':')
                print_dict(v, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix + '\t')
            elif isinstance(v, (np.ndarray, tf.Tensor, torch.Tensor)):
                if type(v) in type_for_print:
                    print(prefix + "{}: {}, {}, {}".format(k, type(v), v.shape, v))
                else:
                    print(prefix + "{}: {}, {}".format(k, type(v), v.shape))
            elif isinstance(v, list) and list in type_for_print and recursive_list:
                print(prefix + k + str(type(v)) + ':')
                for list_v in v:
                    if isinstance(list_v, dict):
                        print_dict(list_v, only_keys, type_for_print, recursive_dict, recursive_list, prefix=prefix + '\t')
                    else:
                        if type(list_v) in type_for_print:
                            print(prefix + '\t' + "{}, {}".format(type(list_v), list_v))
                        else:
                            print(prefix + '\t' + "{}".format(k, type(list_v)))
            else:
                if type(v) in type_for_print:
                    print(prefix + "{}: {}, {}".format(k, type(v), v))
                else:
                    print(prefix + "{}: {}".format(k, type(v)))


data = {"1_1": {"1_1_1": "vege", "1_1_2": "nana"}, "1_2": "semmi", "1_3": {"1_3_1": {"1_3_1_1": "juhu", "1_3_1_2": "wao"}, "1_3_2": "a-a"}}


if __name__ == "__main__":
	print_dict(data, only_keys=False, type_for_print=[str, float, int, list], recursive_dict=True)
