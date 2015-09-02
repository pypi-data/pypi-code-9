
from joblib import Memory
from kegg.lib import get_pathway_to_definition_map
import godb

MEMORY = Memory(cachedir="./")


def get_and_insert_annotations(df, dataset, nb_cpus):

    """Get the definition of each ontology category.

    Gives each ontology category a human readable
    definition.

    Example (term and definition):
    GO:0005706 A thread-like connection joining two regions of ectopically paired
               polytene chromosomes."""

    annotations = get_annotations(df["go_root"], dataset, nb_cpus)

    annotations = annotations.reset_index(drop=True)
    annotations.columns = ["go_root", "go_annotation", "ontology"]

    df = df.reset_index(drop=True)

    return df.merge(annotations, on="go_root")


@MEMORY.cache(verbose=0)
def get_annotations(terms, dataset, nb_cpus):
    """Get annotations for each term in terms."""

    kegg_terms = terms[terms.apply(lambda term: "GO" not in term)]

    go_terms = terms[terms.apply(lambda term: "GO" in term)]

    assert len(kegg_terms) + len(go_terms) == len(terms), \
        "The sum of KEGG and GO terms is not equal to the total number of terms."

    go_annotations = get_annotations_for_go(go_terms)
    kegg_annotations = get_annotations_for_kegg(kegg_terms, dataset)

    annotations = go_annotations.append(kegg_annotations).sort()
    annotations.columns = [0, 1, 2]

    return annotations


@MEMORY.cache(verbose=0)
def get_annotations_for_go(terms):

    """Get the definition of GO terms."""

    df = godb.get_annotations()

    df = df[["GO id", "Term", "Ontology"]]

    df = df[df["GO id"].isin(terms)]

    df.columns = ["go_root", "go_annotation", "ontology"]

    return df.drop_duplicates()


@MEMORY.cache(verbose=0)
def get_annotations_for_kegg(terms, dataset):

    """Get KEGG term definitions from kg Python package."""

    species_to_kegg_map = {"rnorvegicus_gene_ensembl": "rno",
                           "hsapiens_gene_ensembl": "hsa",
                           "mmusculus_gene_ensembl": "mmu"}
    species = species_to_kegg_map[dataset]
    kegg_df = get_pathway_to_definition_map(species)

    kegg_df = kegg_df[["kegg_pathway", "kegg_pathway_definition"]]
    kegg_df = kegg_df[kegg_df["kegg_pathway"].isin(terms)]
    kegg_df["ontology"] = "KG"

    kegg_df.columns = ["go_root", "go_annotation", "ontology"]

    return kegg_df.drop_duplicates()
