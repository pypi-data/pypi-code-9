import sys

import pandas as pd

from godb import get_offspring
from kegg.lib import get_pathway_to_definition_map

from joblib import Memory

MEMORY = Memory(cachedir="./")


@MEMORY.cache(verbose=0)
def create_parent_offspring_maps(ontologies, dataset):

    parent_offspring_maps = []
    for ontology in ontologies:
        parent_offspring_map = create_parent_offspring_map(ontology, dataset)
        parent_offspring_maps.append(parent_offspring_map)

    return pd.concat(parent_offspring_maps, axis=1)


def create_parent_offspring_map(ontology, dataset):

    """Create 2 col long format df where col 1 parent col 2 offspring."""

    if ontology in ["CC", "BP", "MF"]:
        return create_parent_offspring_map_go(ontology)
    elif ontology == "KEGG":
        return create_parent_offspring_map_kegg(dataset)
    else:
        print("Ontology {} not found.".format(ontology))
        sys.exit(1)


@MEMORY.cache(verbose=0)
def create_parent_offspring_map_kegg(species):

    """Get parent offspring map kegg.

    Since KEGG non-hierarchical this is merely a df where the KEGG term in the
    first and second column are the same."""

    # kegg uses a three letter id to denote species; hsa instead of hsapiens,
    # mmu instead of mmusculus etc.
    kegg_id = species[0:3]
    kegg_df = get_pathway_to_definition_map(kegg_id)

    # kegg is not hierarchical so the parent offspring map is just
    # the parent-parent map
    kegg_df = kegg_df[["kegg_pathway", "kegg_pathway"]]
    kegg_df.columns = ["Parent", "Offspring"]
    return kegg_df


@MEMORY.cache(verbose=0)
def create_parent_offspring_map_go(ontology):

    """Get parent offspring map for go terms."""

    df = get_offspring(ontology, relations=["is_a", "part_of"])

    all_terms = pd.Series(list(set(df.ix[:, 0]) | set(df.ix[:, 1])))
    parent_parent = pd.concat([all_terms, all_terms], axis=1)

    cols = ["Offspring", "Parent"]
    df.columns, parent_parent.columns = cols, cols

    return pd.concat([df, parent_parent])
