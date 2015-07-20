__author__ = 'Georgios Rizos (georgerizos@iti.gr)'

import os
import inspect
import multiprocessing
try:
    import cPickle as pickle
except ImportError:
    import pickle

import reveal_graph_embedding


########################################################################################################################
# Configure path related functions.
########################################################################################################################
def get_package_path():
    return os.path.dirname(inspect.getfile(reveal_graph_embedding))


########################################################################################################################
# Configure optimization related functions.
########################################################################################################################
def get_threads_number():
    """
    Automatically determine the number of cores. If that fails, the number defaults to a manual setting.
    """
    try:
        cores_number = multiprocessing.cpu_count()
        return cores_number
    except NotImplementedError:
        cores_number = 8
        return cores_number


def get_file_row_generator(file_path, separator, encoding=None):
    """
    Reads an separated value file row by row.

    Inputs: - file_path: The path of the separated value format file.
            - separator: The delimiter among values (e.g. ",", "\t", " ")
            - encoding: The encoding used in the stored text.

    Yields: - words: A list of strings corresponding to each of the file's rows.
    """
    with open(file_path, encoding=encoding) as file_object:
        for line in file_object:
            words = line.strip().split(separator)
            yield words


def store_pickle(file_path, data):
    """
    Pickle some data to a given path.

    Inputs: - file_path: Target file path.
            - data: The python object to be serialized via pickle.
    """
    pkl_file = open(file_path, 'wb')
    pickle.dump(data, pkl_file)
    pkl_file.close()


def load_pickle(file_path):
    """
    Unpickle some data from a given path.

    Input:  - file_path: Target file path.

    Output: - data: The python object that was serialized and stored in disk.
    """
    pkl_file = open(file_path, 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data
