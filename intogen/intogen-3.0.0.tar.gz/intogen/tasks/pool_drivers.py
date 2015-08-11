import argparse
import logging
from intogen.constants.data_headers import GENE, DRIVER_LABEL, MUTS_PAM_SAMPLE, SIGNALS, POOL_SIGNALS
from intogen.constants.driver_labels import LABEL_MULTISIGNAL, LABEL_1SIG_KNOWN, LABEL_POOL_DRIVER_SUFFIX
from intogen.constants.pandas import ROW_AXIS
from intogen.tasks.gene_results import SIGNAL_MAP
import pandas
from intogen.tasks.intogen_task import IntogenTask
POOL_DRIVER = 'POOL_DRIVER'
INCLUDED_POOL_LABELS = [LABEL_MULTISIGNAL, LABEL_1SIG_KNOWN]


class ConcatTask(IntogenTask):
    def __init__(self):
        super().__init__()
        self.signal_map = SIGNAL_MAP
        self.inverted_signal_map = {v: k for k, v in SIGNAL_MAP.items()}

    @staticmethod
    def get_configuration_definitions():
        return {}

    def run(self, input_file, output_file, pool, thresholds):
        logging.info(input_file)
        logging.info(output_file)
        logging.info(pool)
        logging.info(thresholds)

        wanted_signals = set([self.signal_map[t.upper()] for t in thresholds.keys() if t.upper() in self.signal_map])

        pool_results_df = pandas.read_csv(pool, sep="\t")
        pool_results_df = pool_results_df[pool_results_df[DRIVER_LABEL].isin(INCLUDED_POOL_LABELS)]
        if len(pool_results_df) > 0:
            pool_results_df = pool_results_df[[GENE, DRIVER_LABEL, SIGNALS]]
            pool_results_df[DRIVER_LABEL] = pool_results_df[DRIVER_LABEL] + LABEL_POOL_DRIVER_SUFFIX
            pool_drivers = pool_results_df[GENE].tolist()
        else:
            pool_drivers = []

        recurrencesdf = pandas.read_csv(input_file, sep="\t")
        recurrencesdf = recurrencesdf[[GENE, MUTS_PAM_SAMPLE]]
        recurrencesdf = recurrencesdf[recurrencesdf[GENE].isin(pool_drivers)]

        pooldriven_df = recurrencesdf.merge(pool_results_df)
        if pooldriven_df.shape[0] > 0:
            print(pooldriven_df.head())
            pooldriven_df[POOL_DRIVER] = pooldriven_df.apply(
                lambda row: self.pool_driver(row, thresholds, wanted_signals),
                axis=ROW_AXIS
            )
            pooldriven_df = pooldriven_df[pooldriven_df[POOL_DRIVER] == True]

        pooldriven_df = pooldriven_df[[GENE, DRIVER_LABEL, SIGNALS]]
        pooldriven_df.rename(columns={SIGNALS: POOL_SIGNALS}, inplace=True)
        pooldriven_df.to_csv(output_file, sep="\t", index=False)

    def pool_driver(self, row, thresholds, wanted_signals_set):

        signals_set = set(row[SIGNALS]) & wanted_signals_set
        if len(signals_set) > 0:
            for s in signals_set:
                for key, threshold in thresholds.items():
                    mutated_samples = row[MUTS_PAM_SAMPLE]
                    method_key = self.inverted_signal_map[s].lower()
                    if 0 < mutated_samples < thresholds[method_key]:
                        return True

        return False


def cmdline():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('-p', '--pool', dest='pool')
    parser.add_argument('--thresholds', dest='thresholds')
    options = parser.parse_args()

    # Run the command line
    task = ConcatTask()
    task.run(
        options.input_file,
        options.output_file,
        pool=options.pool,
        thresholds=eval(options.thresholds)
    )


if __name__ == "__main__":
    cmdline()