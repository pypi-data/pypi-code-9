import logging
import bgdata
import sys

DATA_DEPENDENCIES = {
    'bgdata_ensembl': ('intogen', 'ensembl', '1.0'),
    'bgdata_filters': ('intogen', 'filters', '1.0'),
    'bgdata_kegg': ('intogen', 'kegg', '1.0'),
    'bgdata_ma': ('intogen', 'ma', '1.0'),
    'bgdata_mutsigcov': ('intogen', 'mutsigcov', '1.0'),
    'bgdata_networks': ('intogen', 'networks', '1.0'),
    'bgdata_software': ('intogen', 'software', '1.0'),
    'bgdata_transfic': ('intogen', 'transfic', '1.0'),
    'bgdata_genomereference': ('datasets', 'genomereference', 'hg19'),
    'bgdata_vepcache': ('datasets', 'vepcache', '70'),
    'bgdata_liftover': ('datasets', 'liftover', 'hg18_to_hg19')
}


def intogen_setup(download=False):

    # Check and download all dependencies if needed
    for dataset in DATA_DEPENDENCIES.values():
        _check_and_install(dataset, download)


def _check_and_install(dataset, download):
    project, dataset, version = dataset
    if not bgdata.is_downloaded(project, dataset, version):
        if download:
            bgdata.get_path(project, dataset, version)
        else:
            logging.error("You need to run 'intogen --setup' to download or update all the data dependencies.")
            sys.exit(-1)
