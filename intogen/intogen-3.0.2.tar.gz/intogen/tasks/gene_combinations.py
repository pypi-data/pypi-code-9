import argparse
import logging
from intogen.config import get_config
from intogen.constants.data_headers import *
from intogen.constants.driver_labels import DRIVER_LABEL_RANKING
from intogen.tasks import gene_results
from intogen.tasks.intogen_task import IntogenTask
import pandas
from os.path import basename, dirname, join
import numpy as np



def select_highest_label(labels):
    labels = set(labels)
    custom_labels = [l for l in labels if l not in DRIVER_LABEL_RANKING if type(l) is str]
    predefined_and_custom_labels = DRIVER_LABEL_RANKING + custom_labels + ["", None]

    for best in predefined_and_custom_labels:
        if best in labels:
            return best


def aggregate_signals(project_signals):
    signalset = set()
    for signals in project_signals:
        if type(signals) is str:
            signalset.update([s for s in signals])
    all = list(signalset)
    all.sort()
    return "".join(all)


def aggregate_projects(projects):
    p = projects.tolist()
    p.sort()
    return ",".join(p)


class GeneCombinationsTask(IntogenTask):
    @staticmethod
    def get_configuration_definitions():
        return {}


    def run(self, input_files, output_file, grouping_key, group):

        allprojects = []

        out_aggregation = output_file[0]
        out_concat = output_file[1]

        config = get_config()
        concat_df = None
        drivers = set()
        has_pool_signals = False
        for file_name in input_files:
            # load project data
            project_id = basename(dirname(file_name))
            allprojects.append(project_id)
            df = pandas.DataFrame.from_csv(file_name, sep="\t", index_col=None)
            driver_col = df[DRIVER_LABEL]
            driver_col.dropna(inplace=True)
            drivers.update(driver_col.index.tolist())

            # Select wanted data
            muts_cols = [col for col in df.columns.tolist() if "MUTS_" in col]
            results_cols = [col for col in df.columns.tolist() if "VALUE_" in col]
            driver_cols = [GENE, GENE_SYMBOL, SIGNALS, SIGNAL_COUNT, DRIVER_LABEL, KNOWN_DRIVER]
            if POOL_SIGNALS in df.columns:
                driver_cols.append(POOL_SIGNALS)
                has_pool_signals = True
            df = df[driver_cols + muts_cols + results_cols]

            # Concat
            if concat_df is None:
                concat_df = df
            else:
                concat_df = pandas.concat([concat_df, df])
            logging.info("Concatenated data-frames currently size of {}".format(concat_df.shape))

        grouped = concat_df.groupby(GENE)

        aggregated = grouped.agg({
            GENE_SYMBOL: np.max,
            DRIVER_LABEL: lambda labels: select_highest_label(labels),
            MUTS_CS: 'sum',
            MUTS_CS_SAMPLE: 'sum',
            MUTS_PAM: 'sum',
            MUTS_PAM_SAMPLE: 'sum',
            KNOWN_DRIVER: lambda values: values.iloc[0] if len(values) > 0 else "",
            SIGNALS: lambda signals: aggregate_signals(signals),
        })
        if has_pool_signals:
            aggregated = aggregated.join(grouped.agg({
                POOL_SIGNALS: lambda signals: aggregate_signals(signals)
            }))
            print(aggregated.columns.tolist())
            aggregated[SIGNAL_COUNT] = gene_results.highest_signal_count(aggregated[[SIGNALS, POOL_SIGNALS]])
        else:
            aggregated[SIGNAL_COUNT] = aggregated[SIGNALS].apply(gene_results.signal_count)

        aggregated[MUTS_CS] = aggregated[MUTS_CS].astype(int)
        aggregated[MUTS_CS_SAMPLE] = aggregated[MUTS_CS_SAMPLE].astype(int)

        aggregated[MUTS_PAM] = aggregated[MUTS_PAM].fillna(0).astype(int)
        aggregated[MUTS_PAM_SAMPLE] = aggregated[MUTS_PAM_SAMPLE].fillna(0).astype(int)

        #aggregated[PROJECTS_COUNT] = aggregated[PROJECT].apply(lambda row: len(row.split(",")))

        aggregated = aggregated.where(pandas.notnull(aggregated), other=None)
        out_cols = [GENE_SYMBOL, DRIVER_LABEL, SIGNALS, POOL_SIGNALS, SIGNAL_COUNT, MUTS_PAM, MUTS_PAM_SAMPLE, MUTS_CS,
                     MUTS_CS_SAMPLE, KNOWN_DRIVER]
        if not has_pool_signals:
            out_cols.remove(POOL_SIGNALS)
        aggregated = aggregated[out_cols]

        # sort the dataframe (by non-empty columns)
        categs = [l for l in DRIVER_LABEL_RANKING]
        categs.reverse()
        categs += [c for c in pandas.unique(aggregated[DRIVER_LABEL]) if c not in categs and c is not None and c is not '']

        aggregated[DRIVER_LABEL] = aggregated[DRIVER_LABEL].astype("category").cat.set_categories(categs)
        concat_df[DRIVER_LABEL] = concat_df[DRIVER_LABEL].astype("category").cat.set_categories(categs)

        cols_to_sort = [DRIVER_LABEL, SIGNAL_COUNT, MUTS_CS]
        cols_to_sort = [c for c in cols_to_sort if sum(pandas.notnull(aggregated[c])) > 0]

        aggregated = aggregated.sort(cols_to_sort, ascending=False)
        concat_df = concat_df.sort(cols_to_sort, ascending=False)

        allprojects.sort()
        project_series = pandas.Series([PROJECT] + allprojects)
        project_series.to_csv(join(dirname(out_aggregation), 'project_ids.txt'), index=False)

        aggregated.to_csv(out_aggregation, sep="\t")
        concat_df.to_csv(out_concat, sep="\t", index=False)


def cmdline():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='append', dest='input_files', default=[])
    parser.add_argument('-o', dest='output_files', action="append")
    parser.add_argument('--grouping_key', dest='grouping_key')
    parser.add_argument('--group', dest='group')
    options = parser.parse_args()

    # Run the command line
    task = GeneCombinationsTask()
    task.run(
        options.input_files,
        options.output_files,
        grouping_key=options.grouping_key,
        group=options.group
    )


if __name__ == "__main__":
    cmdline()