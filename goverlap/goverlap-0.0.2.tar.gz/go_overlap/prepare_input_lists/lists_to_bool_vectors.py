
from go_overlap.compute_set_overlaps.set_overlaps import \
    compute_non_go_overlaps


def prepare_gene_vectors_for_computation(gene_vectors, all_genes_vector):

    """Turn gene vector(s) into bool lists and compute intersections/diffs.

    First turn vector(s) into bool lists, then, if there are several,
    compute their differences and intersection."""

    bool_vectors = []
    for gene_vector in gene_vectors:
        bool_vector = turn_input_gene_lists_into_bool_vectors(gene_vector,
                                                              all_genes_vector)
        bool_vectors.append(bool_vector)

    return compute_non_go_overlaps(bool_vectors)




def turn_input_gene_lists_into_bool_vectors(gene_vector, all_genes_vector):

    """Turn lists of genes into vectors of bools.

    Turns all gene names into uppercase before comparison to ensure case of gene
    names do not matter."""

    all_genes_vector = all_genes_vector.str.upper()

    gene_vector = gene_vector.str.upper()
    bool_vector = all_genes_vector.isin(gene_vector)

    return bool_vector
