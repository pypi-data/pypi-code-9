import logging

import pandas as pd

from joblib import Memory

from godb.config.settings import CACHE_PATH
from godb.get_and_parse_data.obo_to_df import parse_obo_file

MEMORY = Memory(cachedir=CACHE_PATH)


def _get_all_parent_child_relations(df, ontology, relations=["is_a", "part_of", "has_part"]):

    """Create map of children and parent nodes."""

    children_df = df.loc[df.Ontology == ontology]

    relation_dfs = []
    for relation in relations:

        splitted = children_df[relation].str.split('\t', expand=True)

        stacked = pd.concat([children_df['GO id'], splitted],
                            axis=1).set_index('GO id').stack()

        relation_df = stacked.reset_index().rename(columns={0:relation}).\
                drop('level_1', axis=1)

        empty_col_index = relation_df[relation_df[relation] == ""].index
        relation_df = relation_df.drop(empty_col_index)

        if relation == "part_of":
            relation = "has_part*"
            relation_df.columns = ["GO id", relation]
        elif relation == "has_part":
            relation_df = relation_df[[relation, "GO id"]]
            relation_df.columns = ["GO id", relation]

        relation_df.columns = ["Child", "Parent"]

        relation_df["Relation"] = relation

        relation_dfs.append(relation_df)

    relation_df = pd.concat(relation_dfs)

    return relation_df


def _offspring(children_df):

    """Create long-format df mapping parent and offspring."""

    offspring_df = children_df.copy()[["Child", "Parent"]]
    offspring_df.columns = ["Offspring", "Parent"]

    offspring_df = get_offspring_map(offspring_df)

    return offspring_df


@MEMORY.cache(verbose=0)
def get_offspring_map(df):

    """Turn a map of parent to children into map of parent to offspring.

    I.e. it computes the grandchildren, grand-grandchildren and so on and
    returns a long format dataframe of these relations."""

    logging.info("Computing offspring of node.")
    new_df = _compute_transitive_closure(df)

    while not df.equals(new_df):
        df = df.append(new_df).drop_duplicates()
        new_df = _compute_transitive_closure(df)

        df = df.drop_duplicates().sort()
        new_df = new_df.drop_duplicates().sort()


    return df


def _compute_transitive_closure(df):

    """Computes the transitive closure from a two-col parent/child map."""

    df_temp = df[df["Parent"].isin(df["Offspring"])]
    df2 = df.merge(df_temp, left_on="Offspring", right_on="Parent",
                   suffixes=["_1_gen", "_2_gen"])
    df2 = df2.drop(["Offspring_1_gen", "Parent_2_gen"], axis=1)

    df2.columns = ["Parent", "Offspring"]
    concat_df = pd.concat([df, df2]).drop_duplicates()

    return concat_df

@MEMORY.cache(verbose=0)
def get_children(ontology, relations=["is_a", "part_of", "has_part"], obo_file=""):

    df = parse_obo_file(obo_file)[["is_a", "part_of", "has_part", "GO id", "Ontology"]]

    return _get_all_parent_child_relations(df, ontology, relations).reset_index(drop=True)


@MEMORY.cache(verbose=0)
def get_offspring(ontology, relations=["is_a", "part_of", "has_part"], obo_file=""):

    children = get_children(ontology, relations, obo_file)

    return _offspring(children).reset_index(drop=True)


@MEMORY.cache(verbose=0)
def get_annotations(obo_file=""):

    GOTERM = parse_obo_file(obo_file)[["GO id", "Ontology", "Term",
                                       "Synonym", "Definition"]]

    return GOTERM
