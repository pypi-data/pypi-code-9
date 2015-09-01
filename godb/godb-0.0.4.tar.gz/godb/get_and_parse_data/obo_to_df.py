from __future__ import print_function

import logging
from sys import stderr

import pandas as pd

from godb.config.settings import OBO_PATH, _download_obo_if_not_exists


def parse_obo_file(obo_file=""):

    """Parse obo file into dataframe, where each record takes one row.

    The cols "is_a", and "synonym" are untidy; each may contain more than one
    value per row (each entry is separated by a tab)."""

    if not obo_file:
        obo_file = _download_obo_if_not_exists()

    obo_records = "".join(open(obo_file).readlines()).split("\n\n[Term]")[1:-1]

    record_dicts = []
    for record in obo_records:
        record_dict = _parse_record(record)
        record_dicts.append(record_dict)

    df = pd.DataFrame.from_dict(record_dicts)
    df = _drop_obsolete_records(df)

    df = _clean_dataframe(df).reset_index(drop=True)

    df = df[["id", "namespace", "name", "synonym", "def", "is_a", "part_of", "has_part"]]
    df.columns = ["GO id", "Ontology", "Term", "Synonym", "Definition",
                  "is_a", "part_of", "has_part"]

    return df


def _clean_dataframe(df):

    # Turn names like biological_process into BP.

    df["namespace"] = df["namespace"].apply(
        lambda s: {"biological_process": "BP",
                   "molecular_function": "MF",
                   "cellular_component": "CC"}[s])

    # Turn definitions like:
    #
    # The production of new individuals that contain some portion of
    # genetic material inherited from one or more parent organisms.
    # [GOC:go_curators, GOC:isa_complete, GOC:jl, ISBN:0198506732]
    #
    # into
    #
    # The production of new individuals that contain some portion of
    # genetic material inherited from one or more parent organisms.

    df["def"] = df["def"].apply(lambda s: s.split('" [')[0])
    df["def"] = df["def"].str.replace('"', '')

    df["synonym"] = df["synonym"].str.replace('"', '')

    return df


def _drop_obsolete_records(df):

    obsolete_rows = df.is_obsolete.dropna().index
    df = df.drop(obsolete_rows)
    df.pop("is_obsolete")

    return df


def _parse_record(record, data_to_keep=("id", "name", "namespace", "is_a",
                                        "def", "synonym", "is_obsolete", "relationship")):

    record_lines = record.split("\n")

    synonyms, is_a_list, has_part_list, part_of_list = [], [], [], []
    record_dict = {}

    for line in record_lines:

        if ":" in line:

            key, value = line.split(":", 1)

            if key not in data_to_keep:
                continue

            key, value = key.strip(), value.strip()

            if key == "is_a":
                is_a_list.append(value.split(" !")[0])
            elif key == "synonym":
                synonyms.append(value.split('" ')[0])
            elif key == "relationship":
                relationship_key, relationship_value = value.split(" ", 1)
                if relationship_key == "has_part":
                    has_part_list.append(relationship_value.split(" !")[0])
                elif relationship_key == "part_of":
                    part_of_list.append(relationship_value.split(" !")[0])
            else:
                record_dict[key] = value

        record_dict["is_a"] = "\t".join(is_a_list)
        record_dict["synonym"] = ";".join(synonyms)
        record_dict["has_part"] = "\t".join(has_part_list)
        record_dict["part_of"] = "\t".join(part_of_list)

    return record_dict
