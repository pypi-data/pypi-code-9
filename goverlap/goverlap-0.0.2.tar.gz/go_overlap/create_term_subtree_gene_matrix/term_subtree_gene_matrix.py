import logging
import sys
import pandas as pd
from numpy import uint8, logical_or, array_split
import multiprocessing

from go_overlap.gene_to_terms.terms_to_genes import terms_to_genes
from go_overlap.go_hierarchy.compute_parent_offspring_maps import \
    create_parent_offspring_map

from joblib import Memory


MEMORY = Memory(cachedir="./")

@MEMORY.cache(verbose=0)
def create_gene_subtree_matrix(ontologies, dataset, all_genes_vector, nb_cpus):

    """Create df showing which genes are in which term subtree."""

    non_hierarchical_ontologies = ["KEGG"]

    subtree_to_genes_dfs = []
    for ontology in ontologies:

        parent_offspring_map = create_parent_offspring_map(ontology, dataset)

        all_terms = parent_offspring_map["Offspring"].drop_duplicates()
        terms_to_genes_df = terms_to_genes(ontology, dataset, all_terms)

        nb_terms = len(terms_to_genes_df["Term"].drop_duplicates())
        logging.info("Make term gene map into bool array for the {nb_terms} " \
                     "terms in {ontology} for which associated genes can be " \
                     "found." .format(**vars()))

        terms_to_genes_bool_df = create_gene_list_bool_array(all_genes_vector,
                                                             terms_to_genes_df)
        # terms_to_genes_bool_df["ontology"] = ontology
        if ontology in non_hierarchical_ontologies:
            subtree_to_genes_df = terms_to_genes_bool_df
        else:
            logging.info("Turn term gene bool map into term subtree gene " \
                         "bool map.")
            subtree_to_genes_df = get_all_genes_in_term_subtree(
                parent_offspring_map, terms_to_genes_bool_df, nb_cpus)

        subtree_to_genes_dfs.append(subtree_to_genes_df)

    if len(subtree_to_genes_dfs) > 1:
        return pd.concat(subtree_to_genes_dfs, axis=1)
    elif len(subtree_to_genes_dfs) == 1:
        return subtree_to_genes_dfs[0]


@MEMORY.cache(verbose=0)
def create_gene_list_bool_array(all_genes_vector, gene_term_map):

    """Represent ontology term gene lists as bool vectors."""

    all_terms = gene_term_map["Term"].drop_duplicates()

    gene_bool_vectors = []
    for term in all_terms:
        genes_in_term = gene_term_map[gene_term_map["Term"] == term]["Gene"]
        gene_bool_vector = all_genes_vector.isin(genes_in_term)
        gene_bool_vector.name = term
        gene_bool_vectors.append(gene_bool_vector)

    gene_list_bool_array = pd.concat(gene_bool_vectors, axis=1)

    return gene_list_bool_array.astype(uint8)


def _get_all_genes_in_term_subtree(data_tuple):
    terms, parent_offspring_map, gene_term_map = data_tuple

    subtree_gene_lists = []
    for term in terms:

        # get all offspring terms
        offspring_mask = parent_offspring_map["Parent"] == term
        offspring = parent_offspring_map["Offspring"][offspring_mask]

        # collect all gene vectors from parent and children in list
        subtree_terms = gene_term_map.columns[
            gene_term_map.columns.isin(offspring)]
        gene_vectors = [gene_term_map[t] for t in subtree_terms]

        # Find genes in at least one term in the tree
        subtree_gene_list = reduce(logical_or, gene_vectors)
        subtree_gene_list.name = term
        subtree_gene_lists.append(subtree_gene_list)

    return pd.concat(subtree_gene_lists, axis=1).astype(uint8)


@MEMORY.cache(verbose=0)
def get_all_genes_in_term_subtree(parent_offspring_map, gene_term_map, nb_cpus):

    """Find all genes associated with all terms below term node.

    Needed because we are not interested merely in genes associated with a term
    gene list, but all genes associated with all terms below the term node."""

    if nb_cpus > 1:
        term_arrays = array_split(gene_term_map.columns.drop_duplicates(), nb_cpus)
        data_tuples = [(terms, parent_offspring_map, gene_term_map) for terms in
                    term_arrays]
        pool = multiprocessing.Pool(processes=nb_cpus)
        term_subtree_dfs = pool.map(_get_all_genes_in_term_subtree, data_tuples)
        all_genes_in_term_subtree = pd.concat(term_subtree_dfs, axis=1)
    else:
        all_genes_in_term_subtree = _get_all_genes_in_term_subtree(
            (gene_term_map.columns.drop_duplicates(), parent_offspring_map,
             gene_term_map))

    assert gene_term_map.shape == all_genes_in_term_subtree.shape
    assert gene_term_map.columns.equals(all_genes_in_term_subtree.columns)
    assert gene_term_map.index.equals(all_genes_in_term_subtree.index)

    return all_genes_in_term_subtree


def test__check_term_genes_in_all_genes_vector(all_genes_vector, caplog):

    _check_term_genes_in_all_genes_vector(all_genes_vector, ["a", "X"])
    assert "not found" in caplog.text()


def _check_term_genes_in_all_genes_vector(all_genes_vector, ontology_genes):

    genes_ontologies = set(ontology_genes)
    genes_universe = set(all_genes_vector)

    nb_genes_not_in_universe = len(genes_ontologies - genes_universe)

    if nb_genes_not_in_universe:
        logging.warning("There are {} number of genes associated with your" \
                        " ontologies that are not found in the universe of" \
                        " genes.".format(nb_genes_not_in_universe))
