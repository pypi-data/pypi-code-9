import pandas as pd

def create_gene_list_overlap_df(term_gene_maps, parent_offspring_map):

    for ontology in term_gene_maps:
        term_gene_map = term_gene_maps[ontology]
        overlap_data = get_overlap_data_for_terms(term_gene_map, parent_offspring_map)

        df = pd.DataFrame.from_dict(overlap_data)

    return df


def get_overlap_data_for_terms(term_gene_map, parent_offspring_map):

    overlap_data = []

    for parent, offspring in parent_offspring_map.items():

        genes_related_to_offspring = get_all_genes_related_to_offspring(parent, offspring, term_gene_map)

        overlap_data_for_parent = get_overlap_data(genes_a, genes_b, genes_related_to_offspring, parent)
        overlap_data.append(overlap_data_for_parent)

    return overlap_data


def get_overlap_data(genes_a, genes_b, genes_related_to_offspring, parent):

    a_only, b_only, a_intersect_b = compute_input_genes_overlap(genes_a, genes_b)
    a_intersect_go, b_intersect_go, a_intersect_b_intersect_go = compute_input_genes_ontology_overlap(a_only, b_only,
                                                                                                      a_intersect_b,
                                                                                                      genes_related_to_offspring)

    a_only, b_only, a_intersect_b = len(a_only), len(b_only), len(a_intersect_b)
    a_intersect_go, b_intersect_go, a_intersect_b_intersect_go = len(a_intersect_go), len(b_intersect_go), len(a_intersect_b_intersect_go)
    genes_related_to_offspring = len(genes_related_to_offspring)

    return {"term": parent,
            "a_b": a_intersect_b,
            "a": a_only,
            "b": b_only,
            "a_b_go": a_intersect_b_intersect_go,
            "a_go": a_intersect_go,
            "b_go": b_intersect_go,
            "go": genes_related_to_offspring}

def get_all_genes_related_to_offspring(parent, offspring, term_gene_map):

    all_genes_related_to_offspring_terms = set()

    terms_found = [term for term in offspring if term in term_gene_map]
    for term in terms_found:

        genes_related_to_term = term_gene_map[term]
        all_genes_related_to_offspring_terms.update(genes_related_to_term)

    all_genes_related_to_offspring_terms.add(parent)

    return all_genes_related_to_offspring_terms
