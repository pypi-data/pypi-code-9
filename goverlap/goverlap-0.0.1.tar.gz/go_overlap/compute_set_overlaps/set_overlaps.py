from __future__ import print_function

from numpy import uint8, logical_and, logical_or, array_split, sum as np_sum
from joblib import Memory
import logging
from multiprocessing import Pool
from functools import reduce

import pandas as pd

from go_overlap.gene_to_terms.terms_to_genes import terms_to_genes
from go_overlap.utils.helper_functions import init_worker

MEMORY = Memory(cachedir="./")


@MEMORY.cache(verbose=0)
def compute_go_overlap_matrix(subtree_gene_list, gene_vectors,
                              nb_cpus, experiment_genes=None):

    """Find overlap between input genes and ontology term subtree genes.

    First gets the ontology term to gene maps needed, then computes overlap.

    The final dataframe contains the following columns:

    - go_root: root of the subtree we are computing overlap counts for
    - ontology: ontology "go_root" belongs to
    - a_I_b_I_go: nb genes in a and b and ontology
    - a_M_b_I_go: nb genes in a (but not b) and in ontology
    - b_M_a_I_go: nb genes in b (but not a) and in ontology
    - go_tree: nb genes in subtree of go_root
    - U: nb genes in universe (union of experiment genes and all genes in ontology)
    - a_I_b: nb genes in a and b
    - a_M_b: nb genes in a but not b
    - b_M_a: nb genes in b but not a

    These are used to compute statistics further down the pipeline."""

    #
    logging.info("Find number of genes in both input gene lists and term genes.")
    subtree_overlaps = compute_subtree_overlaps(subtree_gene_list,
                                                gene_vectors, nb_cpus)

    logging.info("Find number of genes in input gene list.")
    non_go_intersections = create_df_from_gene_vectors(gene_vectors,
                                                       subtree_gene_list.columns)
    logging.info("Compute number of genes in universe.")
    genes_in_universe = compute_size_universe(subtree_gene_list,
                                              experiment_genes)
    nb_go_subtree_genes = find_nb_go_subtree_genes(subtree_gene_list)

    logging.info("Concatenating overlap data.")
    df = pd.concat([subtree_overlaps, non_go_intersections, genes_in_universe,
                      nb_go_subtree_genes], axis=1)

    # Making the go term index into a data column
    df = df.reset_index()
    df.rename(columns={"index": "go_root"}, inplace=True)

    return df


def create_df_from_gene_vectors(gene_vectors, indices):
    """Create df of number of genes in input gene lists.

    Each value in each column should be the same."""

    non_go_intersections = pd.concat(gene_vectors, axis=1)
    non_go_intersections = non_go_intersections.sum()
    non_go_intersections = pd.concat([non_go_intersections] * len(gene_vectors),
                                     axis=1)
    non_go_intersections = [non_go_intersections.T.head(1)] * len(indices)
    non_go_intersections = pd.concat(non_go_intersections)

    non_go_intersections = non_go_intersections.set_index(indices)

    return non_go_intersections


def find_nb_go_subtree_genes(subtree_gene_lists):

    """Find the number of genes in each ontology subtree."""

    go_subtree = subtree_gene_lists.sum()
    go_subtree.name = "go_subtree"

    return go_subtree


def compute_size_universe(subtree_gene_lists, experiment_genes):

    """Find number of genes that are either in the experiment or ontologies.

    Use just the total number of genes existing (annotated), if no experiment
    genes given.

    Including the experiment genes is a way to make the p-values less
    conservative."""

    if experiment_genes:
        all_genes_in_ontologies = reduce(subtree_gene_lists, logical_or)
        genes_in_universe = logical_or(all_genes_in_ontologies, experiment_genes)
        nb_genes_in_universe = sum(genes_in_universe)
    else:
        nb_genes_in_universe = len(subtree_gene_lists)

    nb_genes_in_universe = pd.Series(nb_genes_in_universe,
                                     subtree_gene_lists.columns)
    nb_genes_in_universe.name = "U"

    return nb_genes_in_universe


def compute_subtree_overlaps(subtree_gene_list, gene_vectors, nb_cpus):

    """Compute overlap between go term genes and lists of genes.

    TODO: rename internal "subtree_gene_list"; overwrites outer"""

    subtree_gene_list, gene_vectors = _remove_genes_that_cannot_matter(subtree_gene_list,
                                                                       gene_vectors)
    intersected_gene_lists = []
    subtree_gene_lists = array_split(subtree_gene_list, nb_cpus, axis=1)

    pool = Pool(processes=nb_cpus)

    for gene_list in gene_vectors:

        data_tuples = [(gene_list, subtree_gene_list) for subtree_gene_list in
                       subtree_gene_lists]

        intersected_gene_dfs = pool.map(_compute_go_intersections, data_tuples)
        intersected_gene_df = pd.concat(intersected_gene_dfs)

        intersected_gene_lists.append(intersected_gene_df)

    overlap_df = pd.concat(intersected_gene_lists, axis=1)

    return overlap_df

def _remove_genes_that_cannot_matter(go_term_genes, gene_vectors):

    # Remove all genes not in a or b, because they cannot be in the intersection
    # of a and GO (or b and go)

    # this would typically reduce the matrix used from U rows to (a union b) genes
    # a reduction from perhaps 25k to 1k or less, which means time and memory saved

    genes_that_dont_matter = _find_the_genes_that_dont_matter(gene_vectors)

    gene_vectors = [g.drop(genes_that_dont_matter) for g in gene_vectors]
    go_term_genes = go_term_genes.drop(genes_that_dont_matter)

    return go_term_genes, gene_vectors

def _find_the_genes_that_dont_matter(gene_vectors):


    genes_in_at_least_one_list = reduce(logical_or, gene_vectors)
    genes_that_dont_matter = genes_in_at_least_one_list[genes_in_at_least_one_list == False].index

    return genes_that_dont_matter



def _compute_go_intersections(gene_vector_term_genes_array):

    """Compute overlap between go term genes and a list of genes."""

    gene_vector, term_genes_array = gene_vector_term_genes_array
    result_df = logical_and(term_genes_array, gene_vector[:, None])
    result_df.name = gene_vector.name
    result_series = result_df.sum()
    result_series.name = gene_vector.name + "_I_go"

    return result_series


def compute_non_go_overlaps(gene_vectors):

    """Compute overlap intersection and difference between input gene lists."""

    # if only one vector there is no overlap to compute so short circuit
    gene_vectors[0].name = "a"
    if len(gene_vectors) == 1:
        return gene_vectors

    gene_vectors[1].name = "b"

    a, b = gene_vectors
    a_I_b = logical_or(a, b)
    a_I_b.name = "a_I_b"

    a_M_b = a & ~b
    a_M_b.name = "a_M_b"

    b_M_a = b & ~a
    b_M_a.name = "b_M_a"

    return [a, b, a_I_b, a_M_b, b_M_a]
