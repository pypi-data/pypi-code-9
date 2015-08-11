import logging

from intogen.constants.data_headers import GENE, SAMPLE, CHR, START, REF, ALT, MOST_SEVERE_CONSEQUENCE, \
    CONSEQUENCE, MUTSIG_SYM, PVALUE, QVALUE, STRAND
from intogen.constants.pandas import ROW_AXIS
from intogen.constants.qc import ENTITY_GENE, ENTITY_VARIANTS
from intogen.parsers.sequence import complementary_sequence
from intogen.qc.quality_control import QualityControl
from intogen.utils import IntogenStats
import os
import pandas as pd
from intogen.mutsig.preprocess import category


ALT_DUP = ALT + "_dup"

MUTSIG_CATEG = "categ"
MUTSIG_EFFECT = 'effect'
MUTSIG_OUT_GENE = "gene"
MUTSIG_OUT_P_VALUE = "p"
MUTSIG_OUT_Q_VALUE = "q"

EFFECT_NONCODING = "noncoding"
EFFECT_NONSILENT = "nonsilent"
EFFECT_SILENT = "silent"
REQUIRED_MUTS = 50

TEMP_COL = "TEMP"

MAF_FORMAT = 'mutsigMAF'

qc = QualityControl()

class MutsigFileUtils(object):

    @staticmethod
    def check_effect_counts(mutation_effects: pd.Series):
        effect_counts = mutation_effects.value_counts().to_dict()
        try:
            enough_muts = effect_counts[EFFECT_NONCODING] >= 50 and \
                          effect_counts[EFFECT_NONSILENT] >= 50 and \
                          effect_counts[EFFECT_SILENT] >= 50
        except KeyError:
            enough_muts = False
        return effect_counts, enough_muts

    @staticmethod
    def curate_mutations(mutations_file):
        """
        Removes mutations with no category ("---") and checks if enough mutations
        of each effect type are available in the data set (50 min)
        :param mutations_file:
        :return:
        """
        mutations = pd.DataFrame.from_csv(mutations_file, index_col=None, sep="\t")
        mutations = mutations[mutations[MUTSIG_CATEG] != "---"]
        qc.report(ENTITY_VARIANTS, "removed-no-categs", mutations.shape[0])
        mutations.to_csv(mutations_file, sep="\t", index=False)
        # check if n_nonsilent, n_silent & n_noncoding >= 50 - otherwise abort and write empty output
        effect_counts, enough_muts = MutsigFileUtils.check_effect_counts(mutations[MUTSIG_EFFECT])

        return enough_muts, effect_counts





    @staticmethod
    def expand_coverage(full_coverage_file, preprocess_categs, preprocess_coverage_file, output_file):

        logging.info("Expanding coverage to run MutsigCV")

        categs = pd.read_csv(preprocess_categs, sep='\t')
        categs = categs[['name', 'from', 'left', 'change', 'type', 'right']].T.to_dict()

        fc = pd.read_csv(full_coverage_file, sep='\t')
        pc = pd.read_csv(preprocess_coverage_file, sep='\t')

        # Genes at full coverage
        fg = fc[['gene']].drop_duplicates()

        # Genes at preprocess coverage
        pg = pc[['gene']].drop_duplicates()

        # 'Others' genes not present in preprocess coverage
        og = fg[~fg.gene.isin(pg.gene)]

        # Filter non 'Others' full 192 coverage
        fc = fc[fc.gene.isin(og.gene)]

        # Assign preprocess categories
        fc['categ'] = fc.categ.apply(lambda v: category(categs, v[2], v[0], v[7], v[5]))

        aofc = fc.groupby(['gene', MUTSIG_EFFECT, 'categ']).agg({'coverage': 'sum'}).reset_index()
        niofc = fc.groupby(['gene', MUTSIG_EFFECT]).agg({'coverage': 'sum', 'categ': lambda v: 'null+indel'}).reset_index()

        # Concat
        rc = pd.concat([pc, aofc, niofc])

        # Remove 'OTHERS' virtual gene from processed coverage
        frc = rc[rc.gene != 'OTHERS']

        frc.to_csv(output_file, sep='\t', index=False, columns=['gene', MUTSIG_EFFECT, 'categ', 'coverage'])


class MutsigResult(object):
    def __init__(self, mutsig_maf, results_file, gene_filter_path=None):
        """
        @type mutsig_maf: MutsigMAF
        @type results_file: str
        """
        self.mutsig_maf = mutsig_maf
        self.gene_filter_path = None
        self.results = None
        result_muts = 0
        if os.path.exists(results_file):
            self.results = pd.DataFrame.from_csv(results_file, sep="\t", index_col=None)
            result_muts = self.results.shape[0]
        qc.report(ENTITY_GENE, "mutsig-sig-genes", result_muts)



    def convert_and_write(self, out_filename):

        genes_final_results = 0
        if self.results is not None:

            queried_genes = set(self.mutsig_maf.get_data_frame()[MUTSIG_OUT_GENE].tolist())

            data_df = self.results[[MUTSIG_OUT_GENE, MUTSIG_OUT_P_VALUE, MUTSIG_OUT_Q_VALUE]]

            # Generate QQ-Plot
            plotfile = os.path.join(os.path.dirname(out_filename), "gene.mutsig-qqplot.png")
            IntogenStats.qqplot(data_df, "p", plotfile, os.path.dirname(os.path.basename(out_filename)))


            # Only keep results of queried genes
            data_df = data_df[data_df[MUTSIG_OUT_GENE].isin(queried_genes)]
            data_df = data_df.merge(self.mutsig_maf.get_gene_mapping(), left_on=MUTSIG_OUT_GENE, right_on=MUTSIG_SYM)
            data_df[MUTSIG_OUT_GENE] = data_df[GENE]
            data_df.drop(MUTSIG_SYM, axis=1, inplace=True)
            data_df.drop(GENE, axis=1, inplace=True)

            #Rename header according to pipeline standards
            data_df.columns = [GENE, PVALUE, QVALUE]
            data_df.sort([QVALUE], ascending=[1], inplace=True)
            qc.report(ENTITY_GENE, "mutsig-queried", data_df.shape[0])

            # Kick out genes not in white-list (gene_filter)
            if self.gene_filter_path is not None:
                # Get first column of filter file
                filtergenes = pd.DataFrame.from_csv(self.gene_filter_path, sep="\t", index_col=None)
                firstcol = filtergenes.columns[0]
                positive_set = filtergenes[firstcol].tolist()
                # Adjust FDR (non-queried & non-whitelist genes)
                data_df = IntogenStats.filter_andor_recorrect(data_df,
                                                            geneid_col_name=GENE,
                                                            white_list=positive_set)
                qc.report(ENTITY_GENE, "mutsig-whitelisted", data_df.shape[0])


            data_df.to_csv(out_filename, sep="\t", index=False)
            genes_final_results = data_df.shape[0]

        else:
            # Create empty results (no real result found)
            dummy_df = pd.DataFrame(columns=[GENE, PVALUE, QVALUE])
            dummy_df.to_csv(out_filename, sep="\t", index=False)

        qc.report(ENTITY_GENE, "final-results", genes_final_results)

        basename = os.path.basename(self.mutsig_maf.get_filename())
        out_dir = os.path.dirname(out_filename)
        self.mutsig_maf.write(os.path.join(out_dir, basename))


class MutsigMAF(object):
    def __init__(self, variants_file, output_folder, consequence_ranking_file, sym2gene_file, mutsig_muttype_dict_fp, sample_prefix="s_"):
        # Expected in variants file: Gene, Sample, Chr, Position, Change, CT

        self.filename = ''
        self.maf_df = ''
        self.provenance = variants_file
        self.sample_prefix = sample_prefix
        self.consequence_ranking = pd.DataFrame.from_csv(consequence_ranking_file, sep="\t")
        self.mapping = None
        self.enough_muts = False
        self._effect_counts = None

        # Turning off pandas warnings when operating on copies
        pd.options.mode.chained_assignment = None

        # Reading in variants and selecting required columns
        df = pd.read_csv(variants_file, sep='\t', na_values=[''])
        required_cols = [GENE, SAMPLE, CHR, START, REF, ALT, ALT, MOST_SEVERE_CONSEQUENCE, STRAND]
        column_names = [GENE, SAMPLE, CHR, START, REF, ALT, ALT_DUP, MOST_SEVERE_CONSEQUENCE, STRAND]
        self.maf_df = df[required_cols]
        self.maf_df.columns = column_names

        # Remove duplicate (diff. transcripts and filter by most-severe consequence)
        self.maf_df.drop_duplicates(inplace=True)
        self.maf_df.dropna(subset=[MOST_SEVERE_CONSEQUENCE], inplace=True)
        self.maf_df[MOST_SEVERE_CONSEQUENCE] = self.maf_df.groupby([GENE, SAMPLE])[MOST_SEVERE_CONSEQUENCE].transform(self.most_severe)
        self.maf_df.drop_duplicates(inplace=True)
        qc.report(ENTITY_VARIANTS, "most-severe", self.maf_df.shape[0])
        genes_nb = len(set(self.maf_df[GENE].tolist()))
        qc.report(ENTITY_GENE, "most-severe", genes_nb)

        self.mapping = pd.DataFrame.from_csv(sym2gene_file, sep="\t")
        self.mapping = self.mapping[[MUTSIG_SYM, GENE]]
        #self.maf_df.join(mapping, on=GENE)
        self.maf_df = pd.merge(self.maf_df, self.mapping, left_on=GENE, right_on=GENE, sort=False, suffixes=('', '_map'))
        self.maf_df[GENE] = self.maf_df[MUTSIG_SYM]
        self.maf_df.drop(MUTSIG_SYM, axis=ROW_AXIS, inplace=True)

        # Translate variants on - strand to + strand (mutsig expects + always)
        self.maf_df = self.maf_df.apply(self.convert_to_plus_strand, axis=ROW_AXIS)
        self.maf_df.drop(STRAND, axis=ROW_AXIS, inplace=True)

        # Mapping effect
        effect = pd.read_csv(mutsig_muttype_dict_fp, sep="\t")
        logging.debug(self.maf_df.head())
        self.maf_df = pd.merge(self.maf_df, effect, left_on=MOST_SEVERE_CONSEQUENCE, right_on='Variant_Classification')
        self.maf_df.drop('Variant_Classification', axis=1, inplace=True)

        self._effect_counts, self.enough_muts = MutsigFileUtils.check_effect_counts(self.maf_df[MUTSIG_EFFECT])

        out_cols = [MUTSIG_OUT_GENE, "patient", "Chromosome", "Start_position", 'Reference_Allele', 'Tumor_Seq_Allele1',
                    'Tumor_Seq_Allele2', 'Variant_Classification', 'effect']
        self.maf_df.columns = out_cols
        logging.debug(self.maf_df.head())

        qc.report(ENTITY_VARIANTS, "mutsig-input", self.maf_df.shape[0])
        genes_nb = len(set(self.maf_df[MUTSIG_OUT_GENE].tolist()))
        qc.report(ENTITY_GENE, "mutsig-input", genes_nb)

        self.filename = os.path.join(output_folder, os.path.basename(variants_file) + '.' + MAF_FORMAT)
        self.write()
        print('MAF file created: {0}'.format(self.filename))

    def write(self, filename=None):
        if filename is None:
            filename = self.filename
        self.maf_df.to_csv(filename, sep='\t', index=False)

    def get_filename(self):
        return self.filename

    def get_effect_counts(self):
        return self._effect_counts

    def get_data_frame(self):
        return self.maf_df

    def get_gene_mapping(self):
        return self.mapping

    def most_severe(self, group):
        consequences = list(group)
        ranking = self.consequence_ranking[self.consequence_ranking[CONSEQUENCE].isin(consequences)]
        return ranking[CONSEQUENCE].irow(0)

    def convert_to_plus_strand(self, row):
        if row[STRAND] == "-":
            row[REF] = complementary_sequence(row[REF])
            row[ALT] = complementary_sequence(row[ALT])
            row[ALT_DUP] = row[ALT]
        return row

    def collapse_coverage(self, coverage_file, output_file):

        """
            This method will create a new full 192 coverage file but only with the gene and effects
            that are present in this project. And all the others genes are aggregated in a artificial
            gene called OTHERS. This will speed-up the MutsigCV preprocess and all the output will
            be correct except the coverage file. We will need to expand again this OTHERS artificial
            gene with the correct values before we run MutsigCV again.

        :param coverage_file:
        :param output_file:
        """
        logging.info("Collapsing coverage to speedup MutsigCV")
        c = pd.read_csv(coverage_file, sep='\t')
        m = self.maf_df

        valid = m[['gene', 'effect']].drop_duplicates()
        valid = valid[valid.effect != 'null']

        r = c[c['gene'].isin(valid.gene) & c['effect'].isin(valid.effect)]
        o = c[~(c['gene'].isin(valid.gene) & c['effect'].isin(valid.effect))]

        g = o.groupby(['effect', 'categ'])

        a = g.agg({
            'gene': lambda v: "OTHERS",
            'coverage': 'sum'
        })

        b = a.reset_index()
        u = pd.concat([r, b])

        u.to_csv(output_file, sep='\t', index=False, columns=['gene', 'effect', 'categ', 'coverage'])