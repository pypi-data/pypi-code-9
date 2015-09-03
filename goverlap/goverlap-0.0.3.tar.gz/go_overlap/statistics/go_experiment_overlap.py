import logging


def nb_union_genes_in_go_and_experiment(term_to_genes_map_per_ontology, experiment_gene_list):

    number_genes_union_go_experiment = {}

    experiment_genes = set(experiment_gene_list)

    for ontology, term_to_genes_map in term_to_genes_map_per_ontology.items():
        ontology_genes = set()
        for genes in term_to_genes_map.values():
            ontology_genes.update(genes)

        number_total_genes = len(ontology_genes.union(experiment_genes))
        number_genes_union_go_experiment[ontology] = number_total_genes

        logging.info("Number total genes in the union of the experiment genes and ontology {}: {}".format(ontology, number_total_genes))

    return number_genes_union_go_experiment
