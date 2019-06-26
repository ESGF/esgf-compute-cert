import contextlib
import random
import time

import cdms2
import numpy as np
import requests


def validate(truth_path, truth_var_name, process_output):
    with contextlib.ExitStack() as stack:
        truth = stack.enter_context(cdms2.open(truth_path))

        truth_var = truth[truth_var_name]

        output = stack.enter_context(cdms2.open(process_output.uri))

        output_var = output[process_output.var_name]

        for index in truth_var.getAxisListIndex():
            truth_axis = truth_var.getAxis(index)

            output_axis = output_var.getAxis(index)

            assert truth_axis.id == output_axis.id

            assert np.all(truth_axis[:] == output_axis[:])

        samples = random.sample([x for x in range(truth_var.shape[0])], int(truth_var.shape[0]*0.10))

        for index in samples:
            assert np.all(truth_var[index] == output_var[index])


def download(uri, output_path):
    res = requests.get(uri, stream=True)

    res.raise_for_status()

    with open(output_path, 'wb') as outfile:
        for chunk in res.iter_content(chunk_size=8192):
            outfile.write(chunk)


class Timing(object):
    def __init__(self):
        self.start = None
        self.stop = None

    @property
    def elapsed(self):
        return self.stop - self.start

    def __enter__(self):
        self.start = time.time()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop = time.time()
