from sys import exit as sys_exit
from os.path import join as path_join
from subprocess import call

from bioservices import BioMart, BioServicesError
import pandas as pd

from ebs.imports import StringIO

from biomartian.config.cache_settings import memory, default_cache_path


@memory.cache(verbose=0)
def get_marts():

    bm = BioMart(verbose=False)
    """Get available marts and their names."""

    mart_names = pd.Series(bm.names, name="Name")
    mart_descriptions = pd.Series(bm.displayNames, name="Description")

    return pd.concat([mart_names, mart_descriptions], axis=1)


@memory.cache(verbose=0)
def get_datasets(mart):

    bm = BioMart(verbose=False)
    datasets = bm.datasets(mart, raw=True)

    return pd.read_table(StringIO(datasets), header=None, usecols=[1, 2],
                         names = ["Name", "Description"])


@memory.cache(verbose=0)
def get_attributes(mart, dataset):

    if mart == "ensembl" and len(dataset) == 4:
        dataset = convert_ensembl_four_letter_ids(dataset)

    bm = BioMart(verbose=False)
    attributes = bm.attributes(dataset)
    attr_dicts = [{"Attribute": k, "Description": v[0]}
                  for k, v in attributes.items()]
    return pd.DataFrame.from_dict(attr_dicts)


@memory.cache(verbose=0)
def get_bm(intype, outtype, dataset, mart):

    """Queries biomart for data.
    Gets the whole map between INTYPE <-> OUTTYPE and caches it so that disk
    based lookups are used afterwards."""

    if mart == "ensembl" and len(dataset) == 4:
        dataset = convert_ensembl_four_letter_ids(dataset)


    bm = BioMart(verbose=False)

    bm.new_query()

    bm.add_dataset_to_xml(dataset)

    bm.add_attribute_to_xml(intype)
    bm.add_attribute_to_xml(outtype)

    xml_query = bm.get_xml()

    results = bm.query(xml_query)

    map_df = pd.read_table(StringIO(results), header=None, names=[intype,
                                                                  outtype])

    outfile = _get_data_output_filename(intype, outtype, dataset, mart,
                                        default_cache_path=default_cache_path)

    map_df.to_csv(outfile, sep="\t", index=False)

    return map_df


def _get_data_output_filename(intype, outtype, dataset, mart,
                              default_cache_path):

    """Stores a human readable file of biomart query results."""

    filename = "_".join([intype, outtype, dataset, mart]) + ".txt"

    path_name = path_join(default_cache_path, "human_readable")

    call("mkdir -p {}".format(path_name), shell=True)

    outfile = path_join(path_name, filename)

    return outfile

def convert_ensembl_four_letter_ids(abbreviated_id):

    """Gets the ensembl ID using a four letter abbreviation (the prefix)."""

    ids = """oanatinus_gene_ensembl
cporcellus_gene_ensembl
gaculeatus_gene_ensembl
lafricana_gene_ensembl
itridecemlineatus_gene_ensembl
choffmanni_gene_ensembl
csavignyi_gene_ensembl
fcatus_gene_ensembl
rnorvegicus_gene_ensembl
psinensis_gene_ensembl
cjacchus_gene_ensembl
ttruncatus_gene_ensembl
scerevisiae_gene_ensembl
celegans_gene_ensembl
csabaeus_gene_ensembl
oniloticus_gene_ensembl
trubripes_gene_ensembl
amexicanus_gene_ensembl
pmarinus_gene_ensembl
eeuropaeus_gene_ensembl
falbicollis_gene_ensembl
ptroglodytes_gene_ensembl
etelfairi_gene_ensembl
cintestinalis_gene_ensembl
nleucogenys_gene_ensembl
sscrofa_gene_ensembl
ocuniculus_gene_ensembl
dnovemcinctus_gene_ensembl
pcapensis_gene_ensembl
tguttata_gene_ensembl
mlucifugus_gene_ensembl
hsapiens_gene_ensembl
pformosa_gene_ensembl
mfuro_gene_ensembl
tbelangeri_gene_ensembl
ggallus_gene_ensembl
xtropicalis_gene_ensembl
ecaballus_gene_ensembl
pabelii_gene_ensembl
xmaculatus_gene_ensembl
drerio_gene_ensembl
lchalumnae_gene_ensembl
tnigroviridis_gene_ensembl
amelanoleuca_gene_ensembl
mmulatta_gene_ensembl
pvampyrus_gene_ensembl
panubis_gene_ensembl
mdomestica_gene_ensembl
acarolinensis_gene_ensembl
vpacos_gene_ensembl
tsyrichta_gene_ensembl
ogarnettii_gene_ensembl
dmelanogaster_gene_ensembl
mmurinus_gene_ensembl
loculatus_gene_ensembl
olatipes_gene_ensembl
ggorilla_gene_ensembl
oprinceps_gene_ensembl
dordii_gene_ensembl
oaries_gene_ensembl
mmusculus_gene_ensembl
mgallopavo_gene_ensembl
gmorhua_gene_ensembl
aplatyrhynchos_gene_ensembl
saraneus_gene_ensembl
sharrisii_gene_ensembl
meugenii_gene_ensembl
btaurus_gene_ensembl
cfamiliaris_gene_ensembl""".split()

    abbreviated_ids = {_id[:4]: _id for _id in ids}
    ensembl_id = abbreviated_ids[abbreviated_id]

    return ensembl_id
