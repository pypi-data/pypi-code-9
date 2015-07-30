from sys import exit as sys_exit
from os.path import join as path_join
from subprocess import call

from widediaper import R
from biomartian.config.cache_settings import memory, default_cache_path


def set_up_mart(mart, dataset=None, outstream=False):

    r = R(outstream)

    r.load_library("biomaRt")

    if dataset:
        get_mart_command = ('mart <- useMart("{mart}", dataset = "{dataset}")'
                            .format(**vars()))
    else:
        get_mart_command = 'mart <- useMart("{mart}")'.format(mart=mart)

    r(get_mart_command)

    return r


@memory.cache(verbose=0)
def get_marts():

    r = R()
    r.load_library("biomaRt")
    r("marts = listMarts()")
    return r.get("marts")


@memory.cache(verbose=0)
def get_datasets(mart):

    r = set_up_mart(mart)
    r("datasets = listDatasets(mart)")
    return r.get("datasets")


@memory.cache(verbose=0)
def get_attributes(mart, dataset):

    r = set_up_mart(mart, dataset)
    r("attributes = listAttributes(mart)")

    return r.get("attributes")


@memory.cache(verbose=0)
def get_bm(intype, outtype, dataset, mart):

    """Queries biomart for data.
    Gets the whole map between INTYPE <-> OUTTYPE and caches it so that disk
    based lookups are used afterwards."""

    r = set_up_mart(mart, dataset)
    get_command = ("input_output_map_df <- getBM(attributes=c('{input_type}', "
                   "'{output_type}'), mart = mart, values = '*')"
                   .format(input_type=intype, output_type=outtype))

    try:
        r(get_command)
        map_df = r.get("input_output_map_df")
    except IOError:
        print(("No data found for mart '{mart}', dataset '{dataset}' \n"
               "and attributes '{intype}' and '{outtype}'. Aborting."
               .format(**vars())))
        sys_exit(1)

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
