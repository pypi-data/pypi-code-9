
import logging
import sys
import pandas as pd


from go_overlap.go.terms_to_annotation import get_and_insert_annotations
from go_overlap.compute_set_overlaps.set_overlaps import \
    compute_go_overlap_matrix, compute_non_go_overlaps
from go_overlap.create_term_subtree_gene_matrix.term_subtree_gene_matrix import \
    create_gene_subtree_matrix, create_gene_list_bool_array
from go_overlap.prepare_input_lists.lists_to_bool_vectors import \
    prepare_gene_vectors_for_computation

from biomartian.bm_queries.bm_query import get_attributes, get_datasets, get_marts, get_bm

from go_overlap.statistics.stats import compute_statistics, \
find_appropriate_statistical_test


def get_all_genes(dataset, experiment_genes):

    """Return all gene names from biomart."""

    logging.info("Getting all genes from biomart for " + dataset)
    df = get_bm("external_gene_name", "go_id", dataset, "ensembl")
    df = df["external_gene_name"].drop_duplicates()

    # this is only true if experiment genes was given
    if isinstance(experiment_genes, pd.Series):
        df = df[df.str.upper().isin(experiment_genes.str.upper())]

    return df


def reorder_df(df):

    """Reorder the columns for final output.

    The cols in the df are different depending on which stats method was used
    to compare the difference between input lists.
    """

    if "chi_sq" in df:
        reordered_columns = ["go_root", "ontology", "chi_sq_fdr", "a_hpgm_go_fdr", "a_odds", "b_hpgm_go_fdr",
                             "b_odds", "a_I_b_I_go", "a_M_b_I_go", "b_M_a_I_go", "go_subtree", "U", "a_I_b",
                             "a_M_b", "b_M_a", "chi_sq", "test_obs", "b_hpgm_go", "a_hpgm_go", "go_annotation"]
        df = df.sort("chi_sq_fdr")

    elif "fisher" in df:
        reordered_columns = ["go_root", "ontology", "fisher_fdr", "a_hpgm_go_fdr", "a_odds", "b_hpgm_go_fdr",
                             "b_odds",  "a_I_b_I_go", "a_M_b_I_go", "b_M_a_I_go", "go_subtree", "U", "a_I_b",
                             "a_M_b", "b_M_a", "fisher", "b_hpgm_go", "a_hpgm_go", "go_annotation"]
        df = df.sort("fisher_fdr")

    else:
        reordered_columns = ["go_root", "ontology", "a_hpgm_go_fdr", "a_odds", "a", "a_I_go", "go_subtree",
                             "U", "a_hpgm_go", "go_annotation"]
        df = df.sort("a_hpgm_go_fdr")

    df = df[reordered_columns]

    return df

def _remove_go_terms_with_too_many_genes(df, max_genes_prct_limit):

    if max_genes_prct_limit == 0:
        return df

    go_genes_prct_of_u = df.go_subtree / df.U
    go_terms_with_too_many_genes = go_genes_prct_of_u > max_genes_prct_limit

    df = df.drop(df[go_terms_with_too_many_genes].index)

    return df



def main(ontologies, dataset, gene_vectors, experiment_genes, nb_cpus, max_genes_prct_limit):

    # writes command run as first line to stdout
    print("# " + " ".join(sys.argv))

    all_genes_vector = get_all_genes(dataset, experiment_genes)

    bool_vectors = prepare_gene_vectors_for_computation(gene_vectors,
                                                        all_genes_vector)

    gene_subtree_df = create_gene_subtree_matrix(ontologies, dataset,
                                                 all_genes_vector, nb_cpus)


    go_overlap_matrix = compute_go_overlap_matrix(gene_subtree_df, bool_vectors,
                                                  nb_cpus)

    logging.debug("The overlap data looks like:\n {}".format(go_overlap_matrix))

    go_overlap_matrix = _remove_go_terms_with_too_many_genes(go_overlap_matrix, max_genes_prct_limit)

    df = compute_statistics(go_overlap_matrix, gene_vectors)

    logging.debug("Df with stats:\n {}".format(df))

    df = get_and_insert_annotations(df, dataset, nb_cpus)

    logging.debug("Df with annotations:\n {}".format(df))

    df = reorder_df(df)

    logging.debug("Reordered df:\n {}".format(df))

    df.to_csv(sys.stdout, index=False, header=True, sep="\t", quotechar="'")
