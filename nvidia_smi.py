"""Parses nvidia-smi output. Finds memory usage, free GPUs, etc."""
# !/usr/bin/env python3
import os
import sys
import re
import subprocess
from . import console


class NvidiaSmi:
    """Queries GPU info through executing nvidia-smi and stores the result.
    Members:
    * gpu_count
    * gpu_info: list of dict, dict elements:
        "pid": process ids running on that GPU (list)
        "pidmem": memory used by process ids running on that GPU, respectively (in bytes) (list of ints)
        "memtotal": total GPU RAM (bytes)
        "memused": used GPU RAM (bytes)
        "memfree": free GPU RAM (bytes)
    """

    def __init__(self):
        self.gpu_count = 0
        self.gpu_info = {}
        self.update()

    def _parsemem(self, s):
        assert s.endswith("MiB")
        return int(s.replace("MiB", "")) * 1024 * 1024

    def update(self):
        # without this setting, CUDA_VISIBLE_DEVICES may not be consistent with nvidia-smi's numbering
        if "CUDA_DEVICE_ORDER" not in os.environ:
            os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"

        self.gpu_count = 0
        self.gpu_info = {}

        try:
            nv = subprocess.check_output(['nvidia-smi'])
        except (KeyboardInterrupt, NotImplementedError, SystemExit):
            raise  # allow Ctrl+C
        except:
            return

        if not isinstance(nv, str):  # python 3 again...
            nv = nv.decode()
        nv = [line.strip() for line in nv.split("\n")]

        state = "gpus"
        gpuid = None  # current id
        for line in nv:
            if line.find("Processes:") >= 0:
                state = "processes"
            else:
                tok = [x for x in line.split() if x != ""]
                if len(tok) <= 1:
                    continue
                if tok[0] == "|" and re.match("^[0-9]+$", tok[1]):
                    gpuid = int(tok[1])
                    if gpuid not in self.gpu_info:
                        self.gpu_info[gpuid] = {"pid": [], "pidmem": [], "memtotal": 0, "memused": 0, "memfree": 0}
                    self.gpu_count = max(self.gpu_count, gpuid + 1)
                    if state == "processes":
                        pid = int(tok[2])
                        process_mem = self._parsemem(tok[-2])

                        info = self.gpu_info[gpuid]
                        info["pid"].append(pid)
                        info["pidmem"].append(process_mem)
                elif tok[1].endswith("%"):
                    _, fan, temp, perf, pwrusage, _, pwrcap, _, memusage, _, memcap, _, gpuutil, _, _ = tok
                    assert gpuid is not None
                    info = self.gpu_info[gpuid]
                    info["memtotal"] = self._parsemem(memcap)
                    info["memused"] = self._parsemem(memusage)
                    info["memfree"] = info["memtotal"] - info["memused"]
        # convert to list
        self.gpu_info = [self.gpu_info[i] for i in self.gpu_info]

    def dump(self):
        print("GPU count: %s" % self.gpu_count)
        for i in range(self.gpu_count):
            print("GPU %s: %s" % (i, self.gpu_info[i]))

    # Returns a list of integers (GPU ids). Can be empty (if only CPU is allowed).
    def cuda_visible_devices(self):
        if "CUDA_VISIBLE_DEVICES" in os.environ:
            cvdstr = os.environ["CUDA_VISIBLE_DEVICES"]
            cvd = [x.strip() for x in cvdstr.split(",")]
            cvd = [int(x) for x in cvd if x != ""]
            for gpu in cvd:
                assert 0 <= gpu < self.gpu_count, "GPU %s does not exist, select another GPU (CUDA_VISIBLE_DEVICES=%s)" % (
                    gpu, cvdstr)
            return cvd
        else:
            return range(self.gpu_count)

    # Crashes the program if the selected GPUs (CUDA_VISIBLE_DEVICES) are busy.
    # A GPU is busy if it uses more memory than 'memused_max'.
    # if_full: can be "exit", "continue" or "prompt". Action to take if GPU is full.
    def check_gpu(self, memused_max=150 * 1024 * 1024, if_full="prompt"):
        assert if_full in ["exit", "continue", "prompt"]
        cvd = self.cuda_visible_devices()
        if len(cvd) == 0:
            print("Warning: no GPUs visible")
        else:
            print("Visible devices: " + str(cvd))
        for gpu in cvd:
            memused = self.gpu_info[gpu]["memused"]
            if memused > memused_max:
                if if_full == "exit" or (if_full == "prompt" and not console.yes_no_input(
                        "On GPU %s, processes %s use %s bytes. Do you want to use that GPU?" %
                        (gpu, self.gpu_info[gpu]["pid"], memused))):
                    print("Aborted: GPU %s is in use" % gpu)
                    sys.exit(1001)
            else:
                print("GPU %s OK (RAM used: %s bytes)" % (gpu, memused))

    def get_free(self):
        return [i for i in range(len(self.gpu_info)) if not self.gpu_info[i]["pid"]]

    def get_gpu_alloc_list(self, mem_free_if_below=0):
        res = self.get_free()
        res += [i for i in range(len(self.gpu_info)) if
                i not in res and self.gpu_info[i]["memused"] < mem_free_if_below]
        return res


import unittest


class Tests(unittest.TestCase):
    def test(self):
        nv = NvidiaSmi()
        nv.dump()
        assert nv.gpu_count > 0
        for i in range(nv.gpu_count):
            assert nv.gpu_info[i]["memtotal"] > 0
        # check GPU avail
        old_cvd = os.environ.get("CUDA_VISIBLE_DEVICES")
        nv.check_gpu(if_full="continue")
        os.environ["CUDA_VISIBLE_DEVICES"] = "1"
        nv.check_gpu(if_full="continue")
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        nv.check_gpu(if_full="continue")
        if old_cvd is None:
            del os.environ["CUDA_VISIBLE_DEVICES"]
        else:
            os.environ["CUDA_VISIBLE_DEVICES"] = old_cvd
