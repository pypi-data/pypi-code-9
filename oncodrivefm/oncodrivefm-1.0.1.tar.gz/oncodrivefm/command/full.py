import datetime
import os
import os.path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator

from oncodrivefm import tdm
from oncodrivefm.analysis import OncodriveFmAnalysis
from oncodrivefm.command.base import Command
from oncodrivefm.method.factory import create_method
from oncodrivefm.method.empirical import EmpiricalTest
from oncodrivefm.method.zscore import ZscoreTest
from oncodrivefm.mapping import MatrixMapping
from oncodrivefm.utils.labelfilter import LabelFilter


class FullCommand(Command):
    def __init__(self):
        Command.__init__(self, prog="oncodrivefm", desc="Compute the FM bias for genes and pathways")

    def _add_arguments(self, parser):
        Command._add_arguments(self, parser)

        parser.add_argument("data_path", metavar="DATA",
                            help="File containing the data matrix in TDM format")

        parser.add_argument("-N", "--samplings", dest="num_samplings", type=int, default=10000, metavar="NUMBER",
                            help="Number of samplings to compute the FM bias pvalue")

        parser.add_argument("-e", "--estimator", dest="estimator", metavar="ESTIMATOR",
                            choices=["mean", "median"], default="mean",
                            help="Test estimator for computation.")

        parser.add_argument("--gt", "--gene-threshold", dest="mut_gene_threshold", type=int, default=2,
                            metavar="THRESHOLD",
                            help="Minimum number of mutations per gene to compute the FM bias")

        parser.add_argument("--pt", "--pathway-threshold", dest="mut_pathway_threshold", type=int, default=10,
                            metavar="THRESHOLD",
                            help="Minimum number of mutations per pathway to compute the FM bias")

        parser.add_argument("-s", "--slices", dest="slices", metavar="SLICES",
                            help="Slices to process separated by commas")

        parser.add_argument("-m", "--mapping", dest="mapping", metavar="PATH",
                            help="File with mappings between genes and pathways to be analysed")

        parser.add_argument("-f", "--filter", dest="filter", metavar="PATH",
                            help="File containing the features to be filtered. By default labels are includes,"
                                 " labels preceded with - are excludes.")

        parser.add_argument("--save-data", dest="save_data", default=False, action="store_true",
                            help="The input data matrix will be saved")

        parser.add_argument("--save-analysis", dest="save_analysis", default=False, action="store_true",
                            help="The analysis results will be saved")

        parser.add_argument("--pathways_only", dest="pathways_only", default=False, action="store_true",
                            help="Run only the pathways analysis")

        parser.add_argument("--plots", dest="plots", default=False, action="store_true",
                            help="Print plots for quality control")

    def _check_args(self):
        Command._check_args(self)

        if self.args.analysis_name is None:
            self.args.analysis_name, ext = os.path.splitext(os.path.basename(self.args.data_path))

        if self.args.num_samplings < 1:
            self._error("Number of samplings out of range [2, ..)")

        if self.args.mut_gene_threshold < 1:
            self._error("Minimum number of mutations per gene out of range [1, ..)")

        if self.args.mut_pathway_threshold < 1:
            self._error("Minimum number of mutations per pathway out of range [1, ..)")

        if self.args.mapping is not None and not os.path.isfile(self.args.mapping):
            self._error("Pathways mapping file not found: {0}".format(self.args.mapping))

    def run(self):
        Command.run(self)

        # Load filter
        self.filter = LabelFilter()
        if self.args.filter is not None:
            self.log.info("Loading filter ...")
            self.log.debug("  > {0}".format(self.args.filter))

            self.filter.load(self.args.filter)

            self.log.debug("  {0} includes, {1} excludes".format(
                self.filter.include_count, self.filter.exclude_count))

        # Load data

        self.log.info("Loading data ...")
        self.log.debug("  > {0}".format(self.args.data_path))

        # TODO: Support loading plain matrices: /file.tsv#slice=SIFT

        self.matrix = tdm.load_matrix(self.args.data_path)

        self.log.debug("  {0} rows, {1} columns and {2} slices".format(
            self.matrix.num_rows, self.matrix.num_cols, self.matrix.num_slices))

        # Get selected slice indices

        if self.args.slices is not None:
            slices = []
            for name in self.args.slices.split(","):
                name = name.strip()
                if name not in self.matrix.slice_name_index:
                    raise Exception("Slice not found: {0}".format(name))
                slices += [self.matrix.slice_name_index[name]]
        else:
            slices = range(self.matrix.num_slices)

        col_names = [self.matrix.slice_names[i] for i in slices]

        if self.args.save_data:
            for i in slices:
                slice_name = self.matrix.slice_names[i]
                self.log.info("Saving {0} data matrix ...".format(slice_name))
                self.save_matrix(self.args.output_path, self.args.analysis_name, self.args.output_format,
                                 self.matrix.row_names, self.matrix.col_names, self.matrix.data[i],
                                 suffix="data-{0}".format(slice_name))

        if not self.args.pathways_only:
            # GENES ---------------------------------------

            # One to one mapping for genes

            map = {}
            for row_name in self.matrix.row_names:
                if self.filter.valid(row_name):
                    map[row_name] = (row_name,)
            genes_mapping = MatrixMapping(self.matrix, map)
            genes_method_name = "{0}-{1}".format(self.args.estimator, EmpiricalTest.NAME)

            # Analysis for genes

            self.log.info("Analysing genes with '{0}' ...".format(genes_method_name))

            analysis = OncodriveFmAnalysis(
                "oncodrivefm.genes",
                num_samplings=self.args.num_samplings,
                mut_threshold=self.args.mut_gene_threshold,
                num_cores=self.args.num_cores)

            results = analysis.compute(self.matrix, genes_mapping, genes_method_name, slices)

            method = create_method(genes_method_name)

            self.log.info("Adding individual results to results ...")
            # sort genes and slices according to their mapping dicts {name -> index}
            sorted_gene_names = [tup[0] for tup in sorted(genes_mapping.group_name_index.items(), key=operator.itemgetter(1))]
            sorted_slices = [self.matrix.slice_names[s].upper() + "_PVALUE" for s in slices]
            results_pandas = pd.DataFrame(results, columns=sorted_gene_names).transpose()
            results_pandas.sort_index(inplace=True)
            results_pandas.columns = sorted_slices

            # Combination for genes
            self.log.info("Combining analysis results ...")

            combined_results = method.combine(np.ma.masked_invalid(results.T))

            combined_results_pandas = pd.DataFrame(combined_results, columns=sorted_gene_names).transpose()
            combined_results_pandas.columns = method.combination_columns
            combined_results_pandas.sort_index(inplace=True)
            combined_results_pandas._metadata = ['filter', 'test']

            combined_results_pandas = combined_results_pandas.join(results_pandas)
            combined_results_pandas.dropna(how='all', inplace=True)

            self.log.info("Saving genes combined results ...")

            self.save_pandas_matrix(self.args.output_path, self.args.analysis_name, self.args.output_format,
                             genes_mapping.group_names, method.combination_columns, combined_results_pandas,
                             suffix="genes", params=[("slices", ",".join(col_names)), ("method", method.name)])

            # self.save_matrix(self.args.output_path, self.args.analysis_name, self.args.output_format,
            #                  genes_mapping.group_names, method.combination_columns, combined_results.T,
            #                  params=[("slices", ",".join(col_names)), ("method", method.name)], suffix="genes",
            #                  valid_row=lambda row: sum([1 if np.isnan(v) else 0 for v in row]) == 0)

            if self.args.plots:
                self.qqplot(combined_results_pandas, self.args.output_path, self.args.analysis_name, suffix="genes")

        # Exit if there is no mapping
        if self.args.mapping is None:
            return

        # PATHWAYS ---------------------------------------

        # Load pathways mappping

        self.log.info("Loading pathways mapping ...")
        self.log.debug("  > {0}".format(self.args.mapping))

        pathways_mapping = self.load_mapping(self.matrix, self.args.mapping, filt=self.filter)

        self.log.debug("  {0} pathways".format(pathways_mapping.num_groups))

        pathways_method_name = "{0}-{1}".format(self.args.estimator, ZscoreTest.NAME)

        # Analysis for pathways

        self.log.info("Analysing pathways with '{0}' ...".format(pathways_method_name))

        analysis = OncodriveFmAnalysis(
            "oncodrivefm.pathways",
            num_samplings=self.args.num_samplings,
            mut_threshold=self.args.mut_pathway_threshold,
            num_cores=self.args.num_cores)

        results = analysis.compute(self.matrix, pathways_mapping, pathways_method_name, slices)

        method = create_method(pathways_method_name)

        if self.args.save_analysis:
            self.log.info("Saving pathways analysis results ...")
            self.save_splitted_results(
                self.args.output_path, self.args.analysis_name, self.args.output_format,
                self.matrix, pathways_mapping,
                method, results, slices, suffix="pathways")

        # Combination for pathways

        self.log.info("Combining analysis results ...")

        combined_results = method.combine(np.ma.masked_invalid(results.T))

        self.log.info("Saving pathways combined results ...")
        self.save_matrix(self.args.output_path, self.args.analysis_name, self.args.output_format,
                         pathways_mapping.group_names, method.combination_columns, combined_results.T,
                         params=[("slices", ",".join(col_names)), ("method", method.name)], suffix="pathways",
                         valid_row=lambda row: sum([1 if np.isnan(v) else 0 for v in row]) == 0)

    def qqplot(self, data_frame, output_path, analysis_name, suffix=""):
        ## Courtesy of Loris Mularoni

        pvalue_cols = [hit for hit in filter(lambda x:'PVALUE' in x, data_frame.columns)]
        NCOLS = 3
        NROWS = int(len(pvalue_cols) / NCOLS) + 1
        WIDTH = 16
        fig = plt.figure(figsize=(WIDTH, WIDTH / float(NCOLS) * NROWS))
        axs = [plt.subplot2grid((NROWS, NCOLS), (N // NCOLS, N % NCOLS)) for N in range(NCOLS * NROWS)]

        self.log.info("Plotting for {},{} ...".format(analysis_name, suffix))

        upper_limit = -np.log10(1.0/self.args.num_samplings)

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
        output_file = os.path.join(output_path, analysis_name + suffix + ".png")
        plt.savefig(output_file, bbox_inches='tight')


def main():
    FullCommand().run()


if __name__ == "__main__":
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print(end - start)
