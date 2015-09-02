try:
    from functools import lru_cache
except ImportError:
    from repoze.lru import lru_cache


@lru_cache(maxsize=32)
def compute_input_genes_overlap(genes_a, genes_b):

    genes_a, genes_b = set(genes_a), set(genes_b)
    a_only = genes_a - genes_b
    b_only = genes_b - genes_a
    a_intersect_b = (genes_a.intersection(genes_b) - a_only) - b_only

    return a_only, b_only, a_intersect_b


def compute_input_genes_ontology_overlap(a_only, b_only, a_and_b, ontology):

    a_and_ontology = a_only.intersection(ontology)
    b_and_ontology = b_only.intersection(ontology)
    a_and_b_and_ontology = a_and_b.intersection(ontology)

    return a_and_ontology, b_and_ontology, a_and_b_and_ontology
