import argparse
import logging
from intogen.constants.qc import ENTITY_GENE, ENTITY_TRANSCRIPTS, ENTITY_VARIANTS
from intogen.tasks.intogen_task import IntogenTask
from os.path import dirname, join
import pandas as pd
import numpy as np

import sys
from intogen import so
import oncodriveclust.command as command
from intogen.constants.data_headers import *

NON_SYN = 0
SYN = 1

# oncodrive gene excludes causes
GENE_EXC_NOT_FOUND = "N"
GENE_EXC_FILTER = "F"
GENE_EXC_THRESHOLD = "T"
NO_GENE_EXC = ""


class OncodriveClustTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {}


    def run(self, input_file, output_file, samples_threshold=5, gene_transcripts_path=None, gene_filter_path=None):

        # Retrieve input data data-frames and longest transcript per gene
        nonsynonymous_df, synonymous_df, longest_transcripts_df = self.prepare_method_inputs(input_file, gene_transcripts_path)

        # Expression filter

        discarded_filter = []
        positive_set = None
        gene_filter_enabled = gene_filter_path is not None

        if gene_filter_enabled:

            gene_filter_df = pd.DataFrame.from_csv(gene_filter_path, sep="\t", index_col=None)
            firstcol = gene_filter_df.columns[0]
            positive_set = gene_filter_df[firstcol]

            discarded_filter = nonsynonymous_df[~nonsynonymous_df[GENE].isin(positive_set)][GENE].drop_duplicates().tolist()
            nonsynonymous_df = nonsynonymous_df[~nonsynonymous_df[GENE].isin(discarded_filter)]
            synonymous_df = synonymous_df[~synonymous_df[GENE].isin(discarded_filter)]
            longest_transcripts_df = longest_transcripts_df[~longest_transcripts_df[GENE].isin(discarded_filter)]
            self.bulk_quality_control(nonsynonymous_df, "gene-filter")

        # Sample-Mutations threshold filter

        discarded_mutsamples = []

        gene_sample_df = nonsynonymous_df[[GENE, SAMPLE]]
        gene_sample_df.drop_duplicates(inplace=True)
        gene_sample_counts = gene_sample_df.groupby(GENE).size()
        discarded_mutsamples = gene_sample_counts[gene_sample_counts < samples_threshold].index.tolist()

        # Create dataframe for excluded genes

        indices = list(set(discarded_filter) | set(discarded_mutsamples))
        excluded_df = pd.DataFrame(index=indices,
                                   columns=[EXCLUSION_CAUSE])
        if len(discarded_filter) > 0:
            excluded_df.ix[discarded_filter, EXCLUSION_CAUSE] = GENE_EXC_FILTER
        if len(discarded_mutsamples) > 0:
            excluded_df.ix[discarded_mutsamples, EXCLUSION_CAUSE] = GENE_EXC_THRESHOLD

        #Data file names
        base = join(dirname(output_file), "temp")
        nonsyn_file = join(base, "oncodriveclust-nonsyn.tsv")
        syn_file = join(base, "oncodriveclust-syn.tsv")
        cds_file = join(base, "oncodriveclust-transcript-length.tsv")
        excluded_file = join(base, "oncodriveclust-excluded-cause.tsv")

        # Write output files
        nonsynonymous_df.to_csv(nonsyn_file, sep="\t", index=None)
        synonymous_df.to_csv(syn_file, sep="\t", index=None)
        longest_transcripts_df.to_csv(cds_file, sep="\t", index=None)
        excluded_df.to_csv(excluded_file, sep="\t")


        # Execute OncodriveCLUST
        cmd = [
            "oncodriveclust",
            "-c",
            "-m", str(samples_threshold),
            "-o", output_file,
            nonsyn_file,
            syn_file,
            cds_file
        ]

        sys.argv = cmd
        logging.info(" ".join(cmd))
        command.main()

    def bulk_quality_control(self, variants_df : pd.DataFrame, label: str):
        self.quality_control(ENTITY_VARIANTS, label, variants_df.shape[0])
        self.quality_control(ENTITY_TRANSCRIPTS, label, variants_df[TRANSCRIPT].drop_duplicates().shape[0])
        self.quality_control(ENTITY_GENE, label, variants_df[GENE].drop_duplicates().shape[0])

    def prepare_method_inputs(self, input_file: str, transcript_file: str):

        # Load variants and transcript data
        variants = pd.DataFrame.from_csv(input_file, sep="\t", index_col=None)
        variants = variants[[GENE, SAMPLE, TRANSCRIPT, MOST_SEVERE_CONSEQUENCE, PROTEIN_POS]]
        transcript_data = pd.DataFrame.from_csv(transcript_file, sep="\t", index_col=None)

        # Quality control (log)
        self.bulk_quality_control(variants, 'all transcripts')

        # Drop variants that are not going to be needed for analysis
        required_consequences = so.SYNONYMOUS | so.ONCODRIVECLUST
        variants = variants[variants[MOST_SEVERE_CONSEQUENCE].isin(required_consequences)]

        # Quality control (log)
        self.bulk_quality_control(variants, 'required-consequences')

        # Drop transcripts that are not the longest ones
        grouped_transcripts = transcript_data.groupby(GENE, as_index=False)
        transcript_variant_count = variants.groupby(TRANSCRIPT).size()
        longest_transcripts = grouped_transcripts.apply(lambda group: self.select_transcript(group, transcript_variant_count))
        # Some genes have various transcripts that are the same length and longest:


        # Join data and discard short transcripts and null data
        variants = variants[variants[TRANSCRIPT].isin(longest_transcripts[TRANSCRIPT].tolist())]

        # Quality control (log)
        self.bulk_quality_control(variants, 'longest available transcripts')

        synonymous = variants[variants[MOST_SEVERE_CONSEQUENCE].isin(so.SYNONYMOUS)]
        nonsynonymous = variants[~variants[MOST_SEVERE_CONSEQUENCE].isin(so.SYNONYMOUS)]

        return nonsynonymous, synonymous, longest_transcripts

    def select_transcript(self, group : pd.DataFrame, transcript_variant_count: pd.DataFrame):
        """
        Select longest transcript. In case various transcripts are the longest, select the one with more mutations or
        the first.
        :return:
        """
        longest = group[group[CDS_LENGTH] == np.max(group[CDS_LENGTH])]
        if longest.shape[0] > 1:
            wanted_transcripts = longest[TRANSCRIPT].tolist()
            wanted_transcripts = set(transcript_variant_count.index).intersection(set(wanted_transcripts))
            if len(wanted_transcripts) == 0:
                return None
            muts_counts = transcript_variant_count.loc[wanted_transcripts]
            max_muts = muts_counts.max()
            if max_muts is np.nan:
                return None
            selected = muts_counts[muts_counts == max_muts].index.tolist()

            # check if the found longest transcripts have mutations and pick first
            for s in selected:
                if s in muts_counts.index:
                    longest = longest[longest[TRANSCRIPT] == s]
                    break

        return longest

def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--samples_threshold', dest='samples_threshold', default=5, type=int)
    parser.add_argument('--gene_transcripts_path', dest='gene_transcripts_path', default=None)
    parser.add_argument('--gene_filter_path', dest='gene_filter_path', default=None)
    options = parser.parse_args()

    # Run the command line
    task = OncodriveClustTask()
    task.run(
        options.input_file,
        options.output_file,
        samples_threshold=options.samples_threshold,
        gene_transcripts_path=options.gene_transcripts_path,
        gene_filter_path=options.gene_filter_path
    )


if __name__ == "__main__":
    cmdline()