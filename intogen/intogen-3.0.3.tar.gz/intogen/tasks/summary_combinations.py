import argparse
import logging

from intogen.constants.data_headers import *
from intogen.constants.pandas import COLUMN_AXIS, ROW_AXIS
from intogen.tasks.intogen_task import IntogenTask
import os
import pandas


class SummaryCombinationsTask(IntogenTask):
    @staticmethod
    def get_configuration_definitions():
        return {}

    def run(self, input_files, output_file, grouping_key, group):

        concat_df = None

        output_file = output_file[0]

        for summary_file in input_files:

            df = pandas.DataFrame.from_csv(summary_file, sep="\t", index_col=None)

            # Concat
            if concat_df is None:
                concat_df = df
            else:
                concat_df = pandas.concat([concat_df, df])
            logging.info("Concatenated data-frames currently size of {}".format(concat_df.shape))

        concat_df.drop([DRIVERS, GENES_MUTATED], axis=ROW_AXIS, inplace=True)
        summary_df = pandas.DataFrame(concat_df.sum(axis=COLUMN_AXIS)).transpose()
        ID = grouping_key.upper()
        summary_df.columns = [ID] + summary_df.columns.tolist()[1:]
        summary_df[ID].loc[0] = group
        logging.info(summary_df)
        logging.info((os.getcwd()))
        summary_df.to_csv(output_file, sep="\t", index=False)


def cmdline():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='append', dest='input_files', default=[])
    parser.add_argument('-o', dest='output_files', action="append")
    parser.add_argument('--grouping_key', dest='grouping_key')
    parser.add_argument('--group', dest='group')
    options = parser.parse_args()

    # Run the command line
    task = SummaryCombinationsTask()
    task.run(
        options.input_files,
        options.output_files,
        grouping_key=options.grouping_key,
        group=options.group
    )


if __name__ == "__main__":
    cmdline()