import argparse
import logging
from intogen import so
from intogen.config import get_config
from intogen.constants.pandas import ROW_AXIS
from intogen.tasks.intogen_task import IntogenTask
import pandas
import numpy as np
from intogen.constants.data_headers import *


class RecurrencesTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {}

    def do_aggregation(self, data_df, consequence_types, mutation_type, group_by, kegg_path):

        # select data columns
        if type(group_by) is not list:
            group_by = [group_by]
        logging.info("Group by key is: {} ".format(group_by))

        needed_columns = [SAMPLE, START, REF, ALT, MOST_SEVERE_CONSEQUENCE]
        for duplicate_col in set(needed_columns) & set(group_by):
            del needed_columns[needed_columns.index(duplicate_col)]

        data_df = data_df[group_by + needed_columns]

        # select consequence-types
        data_df = data_df[data_df[MOST_SEVERE_CONSEQUENCE].isin(consequence_types)]
        if MOST_SEVERE_CONSEQUENCE not in group_by:
            data_df.drop(MOST_SEVERE_CONSEQUENCE, axis=ROW_AXIS, inplace=True)
            data_df.drop_duplicates(inplace=True)

        #MUTATION types
        MUTS = mutation_type
        MUTS_SAMPLE = mutation_type + MUTS_SAMPLE_suffix

        # Remove NAN values at key columns
        for col in group_by:
            data_df[col].fillna(value='-', inplace=True)

        # Prepare aggregation columns
        data_df[MUTS] = 1
        data_df[MUTS_SAMPLE] = data_df[SAMPLE].astype(str)      #Make sure numeric patient ids are strings
        # Load mapping file
        if kegg_path is not None:
            mapping = pandas.read_csv(kegg_path, sep='\t', header=None, names=group_by + [PATHWAY])
            mapping.drop_duplicates(inplace=True)
            merged = pandas.merge(data_df, mapping, on=group_by)
            grouped = merged.groupby([PATHWAY])
        else:
            # Pandas groupby bug workaround. https://github.com/pydata/pandas/issues/9096
            data_df['GROUPBY_KEY'] = data_df[group_by].apply(lambda x: ':'.join(["{}".format(v) for v in x]), axis=1)
            grouped = data_df.groupby(['GROUPBY_KEY'])

        # Group and agreggate variants by sample and gene
        aggregation = {k: 'first' for k in group_by}
        aggregation[MUTS] = 'sum'
        aggregation[MUTS_SAMPLE] = lambda v: len(np.unique(v))
        data_out = grouped.agg(aggregation)
        data_out.set_index(group_by, inplace=True)

        data_out = data_out[[MUTS, MUTS_SAMPLE]]
        return data_out


    def run(self, input_file, output_file, kegg_path=None, group_by=GENE):

        config = get_config()

        # Load input file
        data_in = pandas.read_csv(input_file, sep='\t')


        # prepare data
        coding_sequence = self.do_aggregation(data_in, so.CODING_REGION, MUTS_CS, group_by, kegg_path)
        protein_affecting = self.do_aggregation(data_in, so.PROTEIN_AFFECTING, MUTS_PAM, group_by, kegg_path)
        logging.info(protein_affecting.columns)

        all = coding_sequence.join(protein_affecting, how='outer')
        # Sort descending by MUTATIONS_SUM
        all.sort(columns=[MUTS_CS], ascending=False, inplace=True)


        # Store output file
        all.to_csv(output_file, sep='\t', na_rep='')


def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--kegg_path', dest='kegg_path')
    parser.add_argument('--group_by', dest='group_by')
    options = parser.parse_args()

    # Run the command line
    task = RecurrencesTask()
    task.run(
        options.input_file,
        options.output_file,
        kegg_path=options.kegg_path,
        group_by=eval(options.group_by)
    )


if __name__ == "__main__":
    cmdline()
