import argparse
import logging
from intogen.constants.data_headers import MUTS_CS_SAMPLE, GENE, TRANSCRIPT, PROTEIN_POS, \
    MOST_SEVERE_CONSEQUENCE, MUTS_CS, MUTS_PAM, MUTS_PAM_SAMPLE, CHR, STRAND, START, REF, ALT, AA_CHANGE
from intogen.tasks.intogen_task import IntogenTask
import pandas
from os.path import basename, dirname, join

class TranscripCombinationsTask(IntogenTask):
    @staticmethod
    def get_configuration_definitions():
        return {}

    def run(self, input_files, output_file, grouping_key, group):

        allprojects = []

        out_aggregation = output_file[0]

        concat_df = None
        for file_name in input_files:
            # load project data
            project_id = basename(dirname(file_name))
            allprojects.append(project_id)
            df = pandas.DataFrame.from_csv(file_name, sep="\t", index_col=None)

            # Concat
            if concat_df is None:
                concat_df = df
            else:
                concat_df = pandas.concat([concat_df, df])
            logging.info("Concatenated data-frames currently size of {}".format(concat_df.shape))

        group_by_cols = [GENE, TRANSCRIPT, CHR, STRAND, START, REF, ALT, PROTEIN_POS, AA_CHANGE, MOST_SEVERE_CONSEQUENCE]

        # Remove NAN values at key columns
        for col in group_by_cols:
            concat_df[col].fillna(value='-', inplace=True)

        # Pandas groupby bug workaround. https://github.com/pydata/pandas/issues/9096
        concat_df['GROUPBY_KEY'] = concat_df[group_by_cols].apply(lambda x: ':'.join(["{}".format(v) for v in x]), axis=1)
        grouped = concat_df.groupby(['GROUPBY_KEY'])

        aggregation = {k: 'first' for k in group_by_cols}
        aggregation.update({
            GENE: 'first',
            MUTS_CS: 'sum',
            MUTS_CS_SAMPLE: 'sum',
            MUTS_PAM: 'sum',
            MUTS_PAM_SAMPLE: 'sum',
        })
        aggregated = grouped.agg(aggregation)

        aggregated[MUTS_CS] = aggregated[MUTS_CS].astype(int)
        aggregated[MUTS_CS_SAMPLE] = aggregated[MUTS_CS].astype(int)

        aggregated[MUTS_PAM] = aggregated[MUTS_PAM].fillna(0).astype(int)
        aggregated[MUTS_PAM_SAMPLE] = aggregated[MUTS_PAM].fillna(0).astype(int)

        aggregated = aggregated.where(pandas.notnull(aggregated), other=None)
        out_cols = group_by_cols + [MUTS_PAM, MUTS_PAM_SAMPLE, MUTS_CS, MUTS_CS_SAMPLE]
        aggregated = aggregated[out_cols]

        # sort the dataframe (by non-empty columns)
        cols_to_sort = [MUTS_CS]
        cols_to_sort = [c for c in cols_to_sort if sum(pandas.notnull(aggregated[c])) > 0]

        aggregated = aggregated.sort(cols_to_sort, ascending=False)
        concat_df = concat_df.sort(cols_to_sort, ascending=False)

        allprojects.sort()
        project_series = pandas.Series(allprojects)
        project_series.to_csv(join(dirname(out_aggregation), 'project_ids.txt'), index=None)

        aggregated.to_csv(out_aggregation, sep="\t", index=False)


def cmdline():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='append', dest='input_files', default=[])
    parser.add_argument('-o', dest='output_files', action="append")
    parser.add_argument('--grouping_key', dest='grouping_key')
    parser.add_argument('--group', dest='group')
    options = parser.parse_args()

    # Run the command line
    task = TranscripCombinationsTask()
    task.run(
        options.input_files,
        options.output_files,
        grouping_key=options.grouping_key,
        group=options.group
    )


if __name__ == "__main__":
    cmdline()