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
def get_attributes(dataset):

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
