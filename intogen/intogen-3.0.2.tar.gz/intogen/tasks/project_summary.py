import argparse

from intogen.constants.data_headers import PROJECT, MUTS_CS, MUTS_PAM, SAMPLE, SAMPLE_SIZE, VARIANTS, GENES_MUTATED, DRIVERS, \
    DRIVER_LABEL, MUTS_CS_DRIVERS, MUTS_PAM_DRIVERS
from intogen.tasks.intogen_task import IntogenTask
import pandas
import numpy


class ProjectSummaryTask(IntogenTask):
    @staticmethod
    def get_configuration_definitions():
        return {}


    def run(self, genes_result_file, variants_file, output_file, project_key):

        summary_dict = {}

        variants = pandas.DataFrame.from_csv(variants_file, sep="\t", index_col=None)
        summary_dict[SAMPLE_SIZE] = len(variants[SAMPLE].unique())
        summary_dict[VARIANTS] = variants.shape[0]
        del(variants)

        gene_results = pandas.DataFrame.from_csv(genes_result_file, sep="\t", index_col=0)
        summary_dict[GENES_MUTATED] = gene_results["MUTS_CS"].dropna().shape[0]
        drivers = gene_results[DRIVER_LABEL].dropna().index.tolist()
        summary_dict[DRIVERS] = len(drivers)
        summary_dict[MUTS_CS] = int(numpy.nansum(gene_results[MUTS_CS]))
        summary_dict[MUTS_PAM] = int(numpy.nansum(gene_results[MUTS_PAM]))
        summary_dict[MUTS_CS_DRIVERS] = int(numpy.nansum(gene_results[MUTS_CS].loc[drivers]))
        summary_dict[MUTS_PAM_DRIVERS] = int(numpy.nansum(gene_results[MUTS_PAM].loc[drivers]))
        del(gene_results)

        summary_df = pandas.DataFrame.from_dict({project_key: summary_dict}).transpose()
        summary_df.index.name = PROJECT

        summary_df.to_csv(output_file, sep="\t")



def cmdline():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_files', action="append")
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--project_key')
    options = parser.parse_args()

    # Run the command line
    task = ProjectSummaryTask()
    task.run(
        options.input_files[0],
        options.input_files[1],
        options.output_file,
        options.project_key
    )


if __name__ == "__main__":
    cmdline()