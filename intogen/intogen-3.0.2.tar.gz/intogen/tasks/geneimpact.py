import argparse
from intogen import so
from intogen.tasks.intogen_task import IntogenTask
from intogen.transfic import TransFIC
import pandas
import numpy as np
from intogen.constants.data_headers import *


def high_impact(impacts):
    value = TransFIC.class_name(np.min([TransFIC.class_value(v) for v in impacts]))
    return value

class GeneImpactTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {}


    def run(self, input_file, output_file):

        data_types = {
            SIFT_SCORE: np.float64, PPH2_SCORE: np.float64, MA_SCORE: np.float64,
            SIFT_TRANSFIC: np.float64, PPH2_TRANSFIC: np.float64, MA_TRANSFIC: np.float64,
            SIFT_CLASS: object, PPH2_CLASS: object, MA_CLASS: object,
            CONSEQUENCE: object
        }

        # Load input file
        data_in = pandas.read_csv(input_file, sep='\t', dtype=data_types)

        # Filter variants with consequence SYNONYMOUS, NON_SYNONYMOUS, STOP, FRAMESHIFT
        data_filtered = data_in[
            data_in.apply(lambda c: so.match(c[CONSEQUENCE].split(','), so.ONCODRIVEFM), axis=1)
        ]

        # Group and agreggate variants by sample and gene
        grouped = data_filtered.groupby([SAMPLE, GENE])
        data_out = grouped.agg({

            SIFT_SCORE: np.max,
            SIFT_TRANSFIC: np.max,
            SIFT_CLASS: high_impact,

            PPH2_SCORE: np.max,
            PPH2_TRANSFIC: np.max,
            PPH2_CLASS: high_impact,

            MA_SCORE: np.max,
            MA_TRANSFIC: np.max,
            MA_CLASS: high_impact,
        })
        # Store output file
        data_out.to_csv(open(output_file, 'w'), sep='\t')


def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', dest='output_file')
    options = parser.parse_args()

    # Run the command line
    task = GeneImpactTask()
    task.run(
        options.input_file,
        options.output_file,
    )


if __name__ == "__main__":
    cmdline()