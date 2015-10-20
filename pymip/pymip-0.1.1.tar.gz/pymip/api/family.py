# -*- coding: utf-8 -*-
from path import path
import ped_parser
import yaml

from pymip.compat import iteritems


class Family(object):

    """Interface to a MIP family.

    Responsibilities include: starting analyses, etc.

    Args:
        base_dir (path): root level path to the top level family dir
        load (bool): initialize loading automatically [default: True]
    """

    def __init__(self, base_dir, load=True):
        super(Family, self).__init__()
        self.base_dir = path(base_dir)
        self.family_id = self.base_dir.basename()

        self.config_path = self.base_dir.joinpath("{}_config.yaml"
                                                  .format(self.family_id))
        self.ped_path = self.base_dir.joinpath("{}_pedigree.txt"
                                               .format(self.family_id))
        self.sampleinfo_path = self.base_dir.joinpath("{}_qc_sampleInfo.yaml"
                                                      .format(self.family_id))

        self.config = {}
        self.ped = None
        self._family = {}
        self._samples = {}

        if load:
            self.load()

    def load(self):
        """Load the class with data from the file system."""
        # parse qc sample info data
        self._load_sampleinfo()

        # load analysis config data
        self._load_config()

        # setup pedigree
        self._load_pedigree()

    @property
    def owner(self):
        """Return the first institute, always >= 1 institute."""
        return self._institutes[0]

    @property
    def collaborators(self):
        """Return all but the first institute (owner)."""
        return self._institutes[1:]

    @property
    def analyzed_at(self):
        """Return the date of when the analysis was run.

        Returns:
            datetime: timestamp for when the analysis was run
        """
        # N.B. already parsed as datetime object by PyYAML
        return self._family['AnalysisDate']

    @property
    def is_complete(self):
        """Check the analysis run status of the family."""
        analysis_run_status = self._family.get('AnalysisRunStatus')

        if analysis_run_status == 'Finished':
            return True

        elif analysis_run_status == 'notFinished':
            return False

    @property
    def is_wgs(self):
        """Check if the analysis is whole genome."""
        # infer this from the absolute path to the sample info file
        return True if 'genomes' in self.base_dir.abspath() else False

    @property
    def human_genome_build(self):
        """Return the human genome reference build."""
        return self._family['HumanGenomeBuild']['Source']

    @property
    def human_genome_version(self):
        """Return the version of the human genome reference build."""
        return self._family['HumanGenomeBuild']['Version']

    @property
    def ready_vcf(self):
        """Return the path to the most complete VCF file."""
        return self._family['VCFFile']['ReadyVcf']['Path']

    @property
    def clinical_vcf(self):
        """Return the path to the clinical VCF file."""
        return self._family['VCFFile']['Clinical']['Path']

    @property
    def research_vcf(self):
        """Return the path to the research VCF file."""
        return self._family['VCFFile']['Research']['Path']

    def gene_lists(self):
        """Return meta data on all gene lists."""
        included_lists = self._family['VCFParser']['SelectFile']['Database']

        return {data['Acronym']: {'name': data['Acronym'],
                                  'version': data['Version'],
                                  'full_name': data.get('CompleteName',
                                                        data['Acronym']),
                                  'date': data.get('Date')}
                for _, data in iteritems(included_lists)}

    def default_genelist_ids(self, ped_key='Clinical_db'):
        """Return a simple list of ids for the default gene lists."""
        ind_lists = (data.extra_info.get(ped_key, '').split(';')
                     for ind_id, data in iteritems(self.ped.individuals))

        # flatten list of lists
        return set(item for sublist in ind_lists for item in sublist)

    def default_genelists(self):
        """Return a simple list of default gene lists."""
        genelist_ids = self.default_genelist_ids()

        return [data for list_id, data in iteritems(self.gene_lists())
                if list_id in genelist_ids]

    def genelist_name(self):
        """Generate stringified caption for default gene lists."""
        default_genelists = self.default_genelists()
        assert len(default_genelists) > 0, 'No default gene lists'

        gene_lists = ("{} ({})".format(gene_list.get('full_name'),
                                       gene_list.get('version'))
                      for gene_list in default_genelists)

        return ' + '.join(gene_lists)

    @property
    def genelist_path(self):
        """Return the master gene list template."""
        reference_dir = path(self.config['referencesDir'])
        template_file = self._family['VCFParser']['SelectFile']['File']

        return reference_dir.joinpath(template_file)

    def chanjo_sample_outputs(self):
        """Return a list of chanjo coverage outputs with samples ids."""
        samples = ((sample_id, data['Program']['ChanjoAnnotate'].values())
                   for sample_id, data in iteritems(self._samples))

        # expect only one chanjo output per sample
        samples_flat = ((sample_id, data[0]) for sample_id, data in samples)

        return [(sample_id, path(data['Bed']['Path']))
                for sample_id, data in samples_flat]

    def chanjo_outputs(self):
        """Return a list of chanjo coverage outputs."""
        return [cov_path for _, cov_path in self.chanjo_sample_outputs()]

    @property
    def pedigree_svgpath(self):
        """Return the path to the Madeline SVG pedigree output."""
        return self._program('Madeline').get('Path')

    def scout_config_clinical(self):
        """Build a clinical Scout config file."""
        base_config = self._scout_config()
        base_config['load_vcf'] = self.clinical_vcf

        return base_config

    def scout_config_research(self):
        """Build a research Scout config."""
        base_config = self._scout_config()
        base_config['load_vcf'] = self.research_vcf

        return base_config

    @property
    def _institutes(self):
        """Return all institutes."""
        return self._family.get('InstanceTag', [])

    def _program(self, program_id, default=None):
        return self._family['Program'].get(program_id, default or {})

    def _load_sampleinfo(self):
        """Load the QC sample info file using YAML parser."""
        try:
            # open and read the (existing) QC metrics file
            with self.sampleinfo_path.open('r') as handle:
                data = yaml.load(handle)

        except IOError:
            # sample info file didn't exist as expected
            error_message = ("QC sample info file not found for {}"
                             .format(self.family_id))
            raise IOError(error_message)

        # only care about loading a subtree of the data
        data_flat = data[self.family_id]
        self._family = data_flat[self.family_id]

        # remove family information subtree
        del data_flat[self.family_id]

        # load the sample specific information
        self._samples = data_flat

    def _load_config(self):
        """Load the MIP config as YAML file."""
        try:
            with self.config_path.open('r') as handle:
                # load the config file as YAML
                self.config = yaml.load(handle)

        except IOError:
            # config file didn't exist as expected
            error_message = ("Config file not found for {this.family_id}"
                             .format(this=self))
            raise IOError(error_message)

    def _load_pedigree(self):
        """Load the pedigree using ``ped-parser``."""
        try:
            # load the pedigree information into ped-parser
            with path(self.ped_path).open('r') as handle:
                self.ped = ped_parser.FamilyParser(handle, family_type='alt',
                                                   cmms_check=False)
        except IOError:
            # pedigree file didn't exist as expected
            error_message = ("Pedigree file not found for {this.family_id}"
                             .format(this=self))
            raise IOError(error_message)

    def _scout_config(self):
        """Build a base Scout config."""
        individuals = {sample_id: {
            'name': sample_id,
            'bam_path': sample['MostCompleteBAM']['Path'],
            'capture_kit': sample.get('Capture_kit', []),
        } for sample_id, sample in iteritems(self._samples)}

        return {
            'load': True,
            'ped': self._family['PedigreeFile']['Path'],
            'igv_vcf': self.ready_vcf,
            'human_genome_build': self.human_genome_build,
            'human_genome_version': self.human_genome_version,
            'owner': self.owner,
            'collaborators': self.collaborators,
            'madeline': self.pedigree_svgpath,
            'coverage_report': None,
            'gene_lists': self.gene_lists(),
            'default_gene_lists': list(self.default_genelist_ids()),
            'individuals': individuals,
        }
