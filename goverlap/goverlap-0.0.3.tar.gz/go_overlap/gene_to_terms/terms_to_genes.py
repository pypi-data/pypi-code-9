import pandas as pd
import logging

from biomartian.bm_queries.bm_query import get_bm
from kegg.lib import get_kegg
from joblib import Memory

MEMORY = Memory(cachedir="./")


def terms_to_genes(ontology, dataset, all_terms):

    """Get the genes belonging to each ontology term."""

    all_terms = pd.Series(all_terms)
    ontology_to_biomart_id = {"CC": "go_id", "MF": "go_id", "BP": "go_id",
                               "REACTOME": "reactome", "KEGG": "kegg"}
    ontology_id = ontology_to_biomart_id[ontology]

    map_df = get_term_to_gene_mapping(ontology_id, dataset)

    requested_genes_only = map_df[map_df["Term"].isin(all_terms)]

    return requested_genes_only


def set_up_r_session_and_get_mart(dataset):

    r_session = R()
    r_session.load_library("biomaRt")

    get_mart_command = 'mart <- useMart("ensembl", dataset="{}")'.format(dataset)
    r_session(get_mart_command)

    return r_session


@MEMORY.cache(verbose=0)
def get_term_to_gene_mapping(ontology_id, dataset):
    """"Get 2 col df with ontology term and related genes."""
    if ontology_id == "kegg":
        logging.info("Getting kegg gene map for " + dataset)
        return get_term_to_gene_mapping_kegg(dataset)
    elif ontology_id == "go_id":
        logging.info("Getting gene ontology gene map for " + dataset)
        go_id = get_bm("external_gene_name", ontology_id, dataset, "ensembl")
        go_id.columns = ["Gene", "Term"]
        go_id = go_id.dropna()
        return go_id


def get_term_to_gene_mapping_kegg(species):

    species = species[:3]

    add_definitions = False
    kegg_df = get_kegg(species, add_definitions)

    kegg_df = kegg_df[["kegg_pathway", "gene"]]
    kegg_df.columns = ["Term", "Gene"]

    return kegg_df
