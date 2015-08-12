import argparse
import logging
from intogen.tasks.intogen_task import IntogenTask
import os
import sys
import oncodrivefm.command.full as oncodrivefm
from intogen.constants.data_headers import *


class OncodriveFMTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {}


    def run(self, input_file, output_file, num_samplings=10000,
            gene_threshold=2, pathway_threshold=10, estimator="mean", cores=3, slice_name=",".join([PPH2_SCORE, MA_SCORE,
                                                                                                     SIFT_SCORE]),
            filter_path=None, kegg_path=None, pathways_only=False, save_analysis=False, plots=False):

        output_folder = os.path.dirname(output_file)

        cmd = [
            "oncodrivefm",
            "-o", output_folder,
            "-n", "oncodrivefm",
            '-N', str(num_samplings),
            "--gene-threshold", str(gene_threshold),
            "--pathway-threshold", str(pathway_threshold),
            "-e", "{0}".format(estimator),
            "-j", str(cores),
            "--slices", "{0}".format(slice_name)]

        if plots:
            cmd += ["--plots"]

        if filter_path is not None:
            cmd += ["--filter", filter_path]

        if kegg_path is not None:
            cmd += ["-m", kegg_path]

        if pathways_only:
            cmd += ["--pathways_only"]

        if save_analysis:
            cmd += ["--save-analysis"]

        cmd += [input_file]

        sys.argv = cmd

        cmd = " ".join(cmd)
        logging.info(cmd)

        oncodrivefm.main()

        # Rename output
        if not pathways_only:
            os.rename(
                os.path.join(output_folder, "oncodrivefm-genes.tsv"),
                os.path.join(output_folder, "gene.oncodrivefm")
            )

        if kegg_path is not None:
            os.rename(
                os.path.join(output_folder, "oncodrivefm-pathways.tsv"),
                os.path.join(output_folder, "pathway.oncodrivefm")
            )


def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--num_samplings', dest='num_samplings', default=10000, type=int)
    parser.add_argument('--gene_threshold', dest='gene_threshold', default=2, type=int)
    parser.add_argument('--pathway_threshold', dest='pathway_threshold', default=10, type=int)
    parser.add_argument('--estimator', dest='estimator', default='mean')
    parser.add_argument('--cores', dest='cores', default=3, type=int)
    parser.add_argument('--slice_name', dest='slice_name', default=",".join([PPH2_SCORE,MA_SCORE,SIFT_SCORE]))
    parser.add_argument('--filter_path', dest='filter_path', default=None)
    parser.add_argument('--kegg_path', dest='kegg_path', default=None)
    parser.add_argument('--pathways_only', dest='pathways_only', default=False, action="store_true")
    parser.add_argument('--save_analysis', dest='save_analysis', default=False, action="store_true")
    parser.add_argument('--plots', dest='plots', default=False, action="store_true")
    options = parser.parse_args()

    # Run the command line
    task = OncodriveFMTask()
    task.run(
        options.input_file,
        options.output_file,
        num_samplings=options.num_samplings,
        gene_threshold=options.gene_threshold,
        pathway_threshold=options.pathway_threshold,
        estimator=options.estimator,
        cores=options.cores,
        slice_name=options.slice_name,
        filter_path=options.filter_path,
        kegg_path=options.kegg_path,
        pathways_only=options.pathways_only,
        save_analysis=options.save_analysis,
        plots=options.plots
    )


if __name__ == "__main__":
    cmdline()
