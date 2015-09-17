import argparse
import logging
from intogen.constants.driver_labels import LABEL_MULTISIGNAL, LABEL_1SIG_KNOWN, LABEL_1SIG_CONNECTED, DRIVER_LABEL_RANKING
import numpy
from intogen.constants.data_headers import *
from intogen.constants.pandas import ROW_AXIS, COLUMN_AXIS
from intogen.constants.qc import ENTITY_GENE
from intogen.tasks.intogen_task import IntogenTask
import pandas as pd
import networkx

pd.options.mode.chained_assignment = None

SIGNAL_MAP = {'MUTSIG': 'R', 'ONCODRIVECLUST': 'C', 'ONCODRIVEFM': 'F'}

def signal_count(value: str):
    if type(value) is str:
        return len(value)
    return 0

def highest_signal_count(df: pd.DataFrame):
    for signal_col in df.columns:
        df[signal_col] = df[signal_col].apply(signal_count)
    return df.max(axis=ROW_AXIS)


class GeneResultsTask(IntogenTask):
    @staticmethod
    def get_configuration_definitions():
        return {"symbol_mapping_file": "file",
                "network_file": "file",
                "known_drivers_file": "file"
        }


    def run(self, input_files, output_file, thresholds):

        exec_args = self.get_exec_config()

        symbol_mapping_file = exec_args["symbol_mapping_file"]
        network_file = exec_args["network_file"]
        known_drivers_file = exec_args["known_drivers_file"]

        dataframes = {}  # data frames dict to be merged

        for file_name in input_files:
            suffix = "_" + file_name.split(".")[1].upper()
            dataframes[suffix] = pd.DataFrame.from_csv(file_name, sep="\t", index_col=0)

        df = self.multi_df_join(dataframes, artificial_collisions=[ZSCORE])
        symdf = pd.DataFrame.from_csv(symbol_mapping_file, sep="\t", index_col=0)
        df = df.join(symdf, how='left')

        # Make driver calling, signal and label assignment
        df[SIGNALS] = self.signals(df, thresholds, SIGNAL_MAP)
        df[SIGNAL_COUNT] = df[SIGNALS].apply(signal_count)
        df[KNOWN_DRIVER] = self.known_drivers(df, known_drivers_file)
        df[CONNECTED_DRIVER] = self.connected_driver(df, network_file)
        df = self.label(df)

        if POOL_SIGNALS in df.columns.tolist():
            # make pool-driver assignment
            pool_df = dataframes["_POOLDRIVEN"]
            df[DRIVER_LABEL] = df[DRIVER_LABEL].combine_first(pool_df[DRIVER_LABEL].astype(str))
            df[SIGNAL_COUNT] = highest_signal_count(df[[SIGNALS, POOL_SIGNALS]])

        # Order df such that most interesting results are on top
        df.sort([DRIVER_LABEL, SIGNAL_COUNT, MUTS_CS], ascending=False, inplace=True)
        df[DRIVER_LABEL].fillna(value="", inplace=True)

        # move put most interesting coluns to front of df
        new_order_1 = [GENE_SYMBOL, DRIVER_LABEL, SIGNALS, SIGNAL_COUNT, KNOWN_DRIVER, POOL_SIGNALS, CONNECTED_DRIVER, MUTS_CS,
                       MUTS_CS_SAMPLE]
        new_order_2 = [x for x in df.columns.tolist() if x not in new_order_1]
        new_order = new_order_1 + new_order_2

        if POOL_SIGNALS not in df.columns.tolist() and POOL_SIGNALS in new_order:
            new_order.remove(POOL_SIGNALS)

        df.index.name = GENE

        self.quality_control(ENTITY_GENE, 'gene-results', df.shape[0])
        df = df[df[MUTS_CS] >= 1]
        self.quality_control(ENTITY_GENE, 'gene-results-pam-only', df.shape[0])

        df[new_order].to_csv(output_file, sep="\t")


    def multi_df_join(self, df_dict, artificial_collisions=[]):
        """
        Takes a list of dataframes with the same primary key (id) and merges the columns, using
        the dictionary keys as suffixes in case there are conflicts with the column names.

        :param df_dict: A dictionary where keys are strings (collision suffixes) and values are DataFrames
        :param artificial_collisions: A list with column names that create an artificial collision suffix is appended
        :return pandas.DataFrame:
        """

        # check if there are colliding column names
        all_columns = []
        for df in df_dict.values():
            all_columns = all_columns + list(df.columns)
        colliding_columns = set([x for x in all_columns if all_columns.count(x) > 1])
        for ac in artificial_collisions:
            colliding_columns.add(ac)

        df = None
        for suffix, input_df in df_dict.items():

            # rename colliding columns
            renamer_dict = {}
            for col in list(input_df.columns):
                if col in colliding_columns:
                    renamer_dict[col] = col + suffix
            input_df.rename(columns=renamer_dict, inplace=True)

            # join columns
            if df is None:
                df = input_df
            else:
                df = df.join(input_df, how='outer')
            logging.debug("Shape is currently: {}".format(df.shape))

        return df

    def signals(self, gene_results, thresholds, signal_map):
        """

        :param gene_results: pd.DataFrame
        :return: pd.Series
        """

        columns = gene_results.columns
        qvalue_cols = [x for x in list(columns) if QVALUE in x]
        qvalue_df = gene_results[qvalue_cols]
        signals_df = qvalue_df.apply(
            lambda col:
            self.apply_cutoff(col,
                              thresholds["_".join(col.name.split("_")[1:]).lower()],
                              signal_map[col.name.split("_")[1]]
            ),
            axis=COLUMN_AXIS
        )

        return signals_df.apply(self.signals_concat, axis=ROW_AXIS)

    def signals_concat(self, row):
        rowlist = row.tolist()
        rowlist.sort()
        signals = "".join(rowlist)
        if signals == "":
            return numpy.NaN
        return signals


    def apply_cutoff(self, column: pd.Series, threshold: float, signal: str):
        bool_column = column <= threshold
        return bool_column.replace(to_replace=[True, False], value=[signal, ""])

    def known_drivers(self, df, known_drivers_file):

        genes_with_results = df.index.tolist()
        known_df = pd.DataFrame.from_csv(known_drivers_file, sep="\t", index_col=None)
        known_df = known_df[known_df[GENE].isin(genes_with_results)]
        known_list = known_df[GENE].tolist()
        known_series = pd.Series([True for x in range(0, len(known_list))], index=known_list)
        return known_series


    def connected_driver(self, df, network_file):
        G = networkx.read_edgelist(network_file, delimiter="\t")

        logging.debug("Network size: ".format(len(G.nodes())))

        high_confidence = df[(df[SIGNAL_COUNT] > 1) | ((df[SIGNAL_COUNT] == 1) & (df[KNOWN_DRIVER]))]
        high_confidence.dropna(subset=[GENE_SYMBOL], inplace=True)
        high_confidence_syms = df[GENE_SYMBOL].tolist()

        min_one_signal = df[(df[SIGNAL_COUNT] > 0)]
        min_one_sig_count = min_one_signal.shape[0]
        high_confidence_count = len(high_confidence_syms)
        if min_one_sig_count > 0 and high_confidence_count > 0:
            min_one_signal.dropna(subset=[GENE_SYMBOL], inplace=True)

            logging.debug("Considering {} min-one-signal genes for connectedness".format(len(min_one_signal)))

            connected_series = min_one_signal.apply(lambda one_signal_gene: self.is_connected(one_signal_gene, G, high_confidence_syms),
                                                    axis=ROW_AXIS)
        else:
            connected_series = pd.Series()
            logging.warning(
                "Not enough putative drivers detected (high-confidence: {}, with-sig:{})".format(high_confidence_count, min_one_sig_count))
        logging.debug("the connected series is: ".format(connected_series))
        return connected_series

    def is_connected(self, row, network, high_confidence_list):
        sym = row[GENE_SYMBOL]
        if sym in network:
            # logging.debug("Testing connectiions for {}".format(sym))
            for neighbor in network.neighbors(sym):
                if neighbor in high_confidence_list:
                    return True
            # No high-confidence neighbor found
            return False
        # Not in network
        return None


    def label(self, df):

        # labels = pd.Series(index=df.index)
        df[DRIVER_LABEL] = pd.Series()

        high_confidence = list(df[df[SIGNAL_COUNT] > 1].index)
        if len(high_confidence) > 0:
            df[DRIVER_LABEL][high_confidence] = LABEL_MULTISIGNAL
        self.quality_control(entity=ENTITY_GENE, label="high_confidence", value=len(high_confidence), list=high_confidence)

        querythose = (df[SIGNAL_COUNT] == 1) & (df[KNOWN_DRIVER])
        if len(high_confidence) > 0:
            querythose &= df[DRIVER_LABEL] != LABEL_MULTISIGNAL
        known = list(df[querythose].index)
        if len(known) > 0:
            df[DRIVER_LABEL][known] = LABEL_1SIG_KNOWN
        self.quality_control(entity=ENTITY_GENE, label="known_drivers", value=len(known), list=known)

        connected = list(df[(df[SIGNAL_COUNT] == 1) & (df[CONNECTED_DRIVER]) & (
            df[DRIVER_LABEL].isin([LABEL_MULTISIGNAL, LABEL_1SIG_KNOWN]) == False)].index)
        if len(connected) > 0:
            df[DRIVER_LABEL][connected] = LABEL_1SIG_CONNECTED
        self.quality_control(entity=ENTITY_GENE, label="connected_drivers", value=len(connected), list=connected)

        categs = [l for l in DRIVER_LABEL_RANKING]
        categs.reverse()
        df[DRIVER_LABEL] = df[DRIVER_LABEL].astype("category").cat.set_categories(categs + [''])

        return df


def cmdline():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='append', dest='input_files', default=[])
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--thresholds', dest='thresholds')
    options = parser.parse_args()

    # Run the command line
    task = GeneResultsTask()
    task.run(
        options.input_files,
        options.output_file,
        thresholds=eval(options.thresholds)
    )


if __name__ == "__main__":
    cmdline()