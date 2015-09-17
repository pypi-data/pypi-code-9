
# This file declares the data headers used in the intogen intermediate and output files.
# Constants (headers) used for a specific input format are to be declared in the class/file where used.


DATA_HEADERS = {}

AA_CHANGE = 'AA_CHANGE'
DATA_HEADERS[AA_CHANGE] = 'Amino acid change in the protein'

ALT = 'ALT'
DATA_HEADERS[ALT] = 'Nucleotide substition alternative'

CHR = 'CHR'
DATA_HEADERS[CHR] = 'Chromosome'

CDS_LENGTH = 'CDS_LENGTH'
DATA_HEADERS[CDS_LENGTH] = 'Coding DNA Sequence length of the gene in nucleotides'

CONNECTED_DRIVER = 'CONNECTED_TO_DRIVER'
DATA_HEADERS[CONNECTED_DRIVER] = 'Is connected to a driver gene'

CONSEQUENCE = 'CONSEQUENCE'
DATA_HEADERS[CONSEQUENCE] = 'Consequence of mutation'

DRIVERS = 'DRIVERS'
DATA_HEADERS[DRIVERS] = 'Number of drivers'

DRIVER_LABEL = 'DRIVER_LABEL'
DRIVER_LABELS = 'DRIVER_LABELS'
DATA_HEADERS[DRIVER_LABEL] = 'The label describing the kind of driver the gene is'
DATA_HEADERS[DRIVER_LABELS] = DATA_HEADERS[DRIVER_LABEL]

EXCLUSION_CAUSE = "EXCLUSION_CAUSE"
DATA_HEADERS[EXCLUSION_CAUSE] = 'Reason for exclusion'

GENE = 'GENE'
DATA_HEADERS[GENE] = 'Gene identifier'

GENES_MUTATED = 'GENES_MUTATED'
DATA_HEADERS[GENES_MUTATED] = 'Number of genes harboring mutations'

KNOWN_DRIVER = 'KNOWN_DRIVER'
DATA_HEADERS[KNOWN_DRIVER] = 'Known driver as e.g. present in CGC'

MA_CLASS = 'MA_CLASS'
DATA_HEADERS[MA_CLASS] = 'Mutation Assessor class'

MA_SCORE = 'MA_SCORE'
DATA_HEADERS[MA_SCORE] = 'Mutation Assessor score'

MA_TRANSFIC = 'MA_TRANSFIC'
DATA_HEADERS[MA_TRANSFIC] = 'Mutation Assessor transfic score'

MOST_SEVERE_CONSEQUENCE = 'MOST_SEVERE'
DATA_HEADERS[MOST_SEVERE_CONSEQUENCE] = 'Most severe consequence type'

MUTS_SAMPLE_suffix = "_SAMPLES"
DATA_HEADERS[MUTS_SAMPLE_suffix] = 'How many samples are mutated in the given group by'

MUTS_CS = 'MUTS_CS'
DATA_HEADERS[MUTS_CS] = 'When aggregating is the total of mutations Coding Sequence'
MUTS_CS_SAMPLE = MUTS_CS + MUTS_SAMPLE_suffix

MUTS_PAM = 'MUTS_PAM'
DATA_HEADERS[MUTS_PAM] = 'When aggregating is the total of mutations Protein Affecting Mutations'
MUTS_PAM_SAMPLE = MUTS_PAM + MUTS_SAMPLE_suffix

MUTS_CS_DRIVERS = 'MUTS_CS_DRIVERS'
DATA_HEADERS[MUTS_CS_DRIVERS] = 'Number of CS mutations in driver genes'

MUTS_PAM_DRIVERS = 'MUTS_PAM_DRIVERS'
DATA_HEADERS[MUTS_PAM_DRIVERS] = 'Number of PAM mutations in driver genes'


MUTSIG_SYM = 'MUTSIG_SYM'
DATA_HEADERS[MUTSIG_SYM] = 'The gene symbol, as used in the mutsig reference files'

PATHWAY = 'PATHWAY'
DATA_HEADERS[PATHWAY] = 'KEGG pathway identifier'

POOL_SIGNALS = 'POOL_SIGNALS'
DATA_HEADERS[POOL_SIGNALS] = 'is the designated gene a driver in the Pool?'

PPH2_CLASS = 'PPH2_CLASS'
DATA_HEADERS[PPH2_CLASS] = 'Polyphen 2 class'

PPH2_SCORE = 'PPH2_SCORE'
DATA_HEADERS[PPH2_SCORE] = 'Polyphen 2 score'

PPH2_TRANSFIC = 'PPH2_TRANSFIC'
DATA_HEADERS[PPH2_TRANSFIC] = 'Polyphen 2 transfic score'

PROTEIN_POS = 'PROTEIN_POS'
DATA_HEADERS[PROTEIN_POS] = 'Protein position of AA change'

PROTEIN = 'PROTEIN'
DATA_HEADERS[PROTEIN] = 'Protein identifier'

PROJECT = 'PROJECT'
DATA_HEADERS[PROJECT] = 'Poject id(s) where info is coming from'

PROJECTS_COUNT = 'PROJECTS_COUNT'
DATA_HEADERS[PROJECTS_COUNT] = 'Number of projects'


PVALUE = 'PVALUE'
DATA_HEADERS[PROJECTS_COUNT] = 'A p-value'

QVALUE = 'QVALUE'
DATA_HEADERS[QVALUE] = 'A q-value'

RANK = 'RANK'
DATA_HEADERS[RANK] = 'Rank - e.g. of consequence types'
REF = 'REF'
DATA_HEADERS[REF] = 'Reference of nucleotide substitution'

SAMPLE = 'SAMPLE'
DATA_HEADERS[SAMPLE] = 'Sample identifier'

SAMPLE_SIZE = "SAMPLE_SIZE"
DATA_HEADERS[SAMPLE_SIZE] = 'Number of samples for the concerning project/cohort'

SIFT_CLASS = 'SIFT_CLASS'
DATA_HEADERS[SIFT_CLASS] = 'Sift class'

SIFT_SCORE = 'SIFT_SCORE'
DATA_HEADERS[SIFT_SCORE] = 'Sift score'

SIFT_TRANSFIC = 'SIFT_TRANSFIC'
DATA_HEADERS[SIFT_TRANSFIC] = 'Sift transfic score'

SIGNALS = 'SIGNALS'
DATA_HEADERS[SIGNALS] = 'Which signals have been detected: [RCF]'

SIGNAL_COUNT = 'SIGNAL_COUNT'
DATA_HEADERS[SIGNAL_COUNT] = 'Number of signals - significantly identified by methods'

START = 'START'
DATA_HEADERS[START] = 'Start of gene'

STOP = 'STOP'
DATA_HEADERS[STOP] = 'End/stop of gene'

STRAND = 'STRAND'
DATA_HEADERS[STRAND] = 'Strand of gene'

GENE_SYMBOL = 'SYMBOL'
DATA_HEADERS[GENE_SYMBOL] = 'official symbol of gene approved by HGNC'

TRANSCRIPT_IMPACT_CLASS = 'TRANSCRIPT_IMPACT_CLASS'
DATA_HEADERS[TRANSCRIPT_IMPACT_CLASS] = 'Impact class label'

TRANSCRIPT_IMPACT = 'TRANSCRIPT_IMPACT'
DATA_HEADERS[TRANSCRIPT_IMPACT] = 'Impact of transcript in question'

TRANSCRIPT = 'TRANSCRIPT'
DATA_HEADERS[TRANSCRIPT] = 'Transcript identifier'

UNIPROT = 'UNIPROT'
DATA_HEADERS[UNIPROT] = 'Uniprot identifier'

VARIANTS = 'VARIANTS'
DATA_HEADERS[VARIANTS] = 'Number of variants'

ZSCORE = 'ZSCORE'
DATA_HEADERS[ZSCORE] = 'General - Zscore'
