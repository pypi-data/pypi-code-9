import logging
import math
import os
import re
import io
import datetime
from ruffus.ruffus_utility import shorten_filenames_encoder, get_strings_in_nested_sequence
import tempfile
import pandas as pd
import numpy as np
from statsmodels.sandbox.stats.multicomp import fdrcorrection0
import matplotlib.pyplot as plt


def get_nested(d: dict, path: list):
    # for each hierarchy level in path
    for p in path:
        if p not in d:
            return None

        # step into hierarchy
        d = d[p]

    return d


def set_nested(nested_dict: dict, path: list, value):
    level = 0
    d = nested_dict
    # for each hierarchy level in path
    for p in path:
        level += 1

        # if last level, set value, else create dict
        if p not in d and level < len(path):
            d[p] = {}
        elif level == len(path):
            d[p] = value

        # step into hierarchy
        d = d[p]

    return nested_dict


def check_file_exists_and_mod_time(inputs, outputs, *args, **kwargs):
    # logging.debug("Check if task need update")

    inputs = get_strings_in_nested_sequence(inputs)
    outputs = get_strings_in_nested_sequence(outputs)
    #logging.debug(inputs)
    #logging.debug(outputs)

    #
    # build: missing output file
    #
    if len(outputs) == 0:
        return True, "Missing output file"

    # missing input / output file means always build
    missing_files = []
    for io in (inputs, outputs):
        for p in io:
            if not os.path.exists(p):
                missing_files.append(p)
    if len(missing_files):
        return True, "Missing file%s\n        %s" % ("s" if len(missing_files) > 1 else "", shorten_filenames_encoder(missing_files, -55))

    check_time = kwargs["check_time"] if "check_time" in kwargs else True
    if check_time:
        # newest input
        newest_in = 0
        newest_in_path = ""
        for filepath in inputs:
            mtime = os.path.getmtime(filepath)
            #logging.debug("last mod in: {} ({})".format(time.ctime(mtime),filepath))
            if mtime > newest_in:
                newest_in = mtime
                newest_in_path = filepath

        time_delta = 10  #2*60
        # any of the outputs older than newest input?
        oldest_out_paths = []
        for filepath in outputs:
            mtime = os.path.getmtime(filepath)
            #logging.debug("last mod out: {} ({})".format(time.ctime(mtime), filepath))
            if mtime < newest_in - time_delta:
                oldest_out_paths.append(filepath)

        if len(oldest_out_paths) > 0:
            return True, "Old output files%s\n        %s" % (
                "s" if len(oldest_out_paths) > 1 else "", shorten_filenames_encoder(oldest_out_paths, -55))

    return False, "File {0} exists".format(outputs)


def check_file_exists_old(input_file, output_file, *args):
    outputs = output_file if not isinstance(output_file, str) else [output_file]

    if len(outputs) == 0:
        return True, "Missing output file"

    for file in outputs:
        if not os.path.exists(file):
            return True, "Missing file %s" % file

    return False, "File {0} exists".format(output_file)


VALID_PROJECT_NAME = re.compile("[^a-z0-9_]", re.IGNORECASE)


def scheduler(*args):
    keys = []
    prefix = None
    for key in args:
        scheduler_key = VALID_PROJECT_NAME.sub('', key).lower()
        if prefix is not None:
            scheduler_key = '.'.join([prefix, scheduler_key])
        keys.append(scheduler_key)
        prefix = scheduler_key

    return list(reversed(keys))


class CommentedFile(io.TextIOWrapper):
    def __init__(self, f, mode="r", values=None, comments=None, commentchar="#", writedate=True):
        super().__init__(io.FileIO(f, mode))

        self.values = values
        self.comments = comments

        self._commentchar = commentchar

        if writedate:
            if comments is None:
                comments = []

            comments.append(str(datetime.datetime.today()))

        self.writedHeader = False

    def read(self, *args, **kwargs):
        line = super().readline()
        while line.startswith(self._commentchar):
            if line.startswith(self._commentchar + self._commentchar):
                if self.values is None:
                    self.values = {}
                k, v = line.replace(self._commentchar + self._commentchar + " ", "").split("=")
                self.values[k.strip()] = v.strip()
            else:
                if self.comments is None:
                    self.comments = []
                self.comments.append(line.replace(self._commentchar, "").strip())
            line = super().readline()

        return line

    def write(self, *args, **kwargs):

        # First write the header comments
        if not self.writedHeader:

            if self.comments is not None:
                super().write("\n".join([self._commentchar + " " + comment for comment in self.comments]))
                super().write("\n")

            if self.values is not None:
                super().write("\n".join([self._commentchar + self._commentchar + " " + str(k) + "=" + str(v) for k, v in self.values.items()]))
                super().write("\n")

            self.writedHeader = True

        super().write(*args, **kwargs)

    def __iter__(self):
        return self




"""
Returns a temp folder
"""


def get_temp_folder(base_dir=tempfile.gettempdir()):
    # Create a directory for temporary files

    if not os.path.exists(base_dir):
        base_dir = tempfile.gettempdir()

    tmp_dir = tempfile.mkdtemp(dir=base_dir, prefix="intogen-")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    return tmp_dir


"""
Returns a temp file
"""


def get_temp_file(base_dir=tempfile.gettempdir()):
    if not os.path.exists(base_dir):
        base_dir = tempfile.gettempdir()

    # Create a directory for temporary files
    return tempfile.mkstemp(dir=base_dir, prefix="intogen-")


class IntogenStats():
    @staticmethod
    def get_fdr(series):
        na_indexes = series[series.isnull()].index
        not_na_indexes = series[np.invert(series.isnull())].index

        corrected_values = fdrcorrection0(series[not_na_indexes])[1]
        corrected_series = pd.Series(corrected_values, index=not_na_indexes)

        corrected_series = corrected_series.append(pd.Series([np.nan] * len(na_indexes), index=na_indexes))

        return corrected_series

    @staticmethod
    def filter_andor_recorrect(df: pd.DataFrame,
                             geneid_col_name: str,
                             white_list: list,
                             pval_col_name: str=None,
                             qval_col_name: str=None):
        df = df[df[geneid_col_name].isin(white_list)]
        if pval_col_name is not None and qval_col_name is not None:
            df[qval_col_name] = IntogenStats.get_fdr(df[pval_col_name])
        return df

    @staticmethod
    def qqplot(data_frame, pvalue_cols, output_path, analysis_name, suffix=""):
        ## Courtesy of Loris Mularoni

        if type(pvalue_cols) is not list:
            pvalue_cols = [pvalue_cols]

        NCOLS = min(3, len(pvalue_cols))
        NROWS = math.ceil(len(pvalue_cols) / NCOLS)
        WIDTH = 16
        fig = plt.figure(figsize=(WIDTH, WIDTH / float(NCOLS) * NROWS))
        axs = [plt.subplot2grid((NROWS, NCOLS), (N // NCOLS, N % NCOLS)) for N in range(NCOLS * NROWS)]

        logging.info("Plotting for {},{} ...".format(analysis_name, suffix))

        #upper_limit = -np.log10(1.0/self.args.num_samplings)
        upper_limit = 15

        for i, pvalue_col in enumerate(pvalue_cols):
            ylabel = pvalue_col
            ax = axs[i]
            obs_pvalues = data_frame[pvalue_col].map(lambda x: -np.log10(x))
            obs_pvalues.sort()
            exp_pvalues = -1 * np.log10(np.arange(1, len(data_frame) + 1) / float(len(data_frame)))
            exp_pvalues.sort()
            ax.scatter(exp_pvalues, obs_pvalues, alpha=0.5)
            ax.set_xlabel("expected pvalues")
            ax.set_ylabel("observed pvalues")
            ax.plot(np.linspace(0, upper_limit), np.linspace(0, upper_limit), 'r--')
            ax.set_xlim(-0.2, upper_limit)
            ax.set_ylim(-0.2, upper_limit)
            ax.set_title("{} ({})".format(pvalue_col, analysis_name))
            ax.set_ylabel(ylabel)

        plt.tight_layout()

        suffix = "-" + suffix if len(suffix) > 0 else ""
        output_file = output_path
        plt.savefig(output_file, bbox_inches='tight')

