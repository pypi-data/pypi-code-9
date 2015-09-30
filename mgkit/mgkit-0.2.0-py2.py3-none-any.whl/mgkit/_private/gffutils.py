from mgkit.io import gff
import pandas as pd
import math
from shapely import geometry
import numpy as np
import seaborn as sns
import mgkit.counts as mcounts
import itertools

bac_id = 2
arc_id = 2157
fun_id = 4751

load_htseq = mcounts.load_htseq_counts


def add_counts(infos, iterator, tx, anc_id=None, rank=None, gene_map=None, ex_anc_id=None):
    newcounts = {}
    for uid, count in iterator:
        try:
            gene_id, taxon_id = infos[uid]
        except KeyError:
            continue

        if gene_map is not None:
            try:
                gene_ids = gene_map[gene_id]
            except KeyError:
                continue
        else:
            gene_ids = [gene_id]

        if ex_anc_id is not None:
            if tx.is_ancestor(taxon_id, ex_anc_id):
                continue
        if anc_id is not None:
            if not tx.is_ancestor(taxon_id, anc_id):
                continue
        if rank is not None:
            taxon_id = tx.get_ranked_taxon(taxon_id, rank).taxon_id

        for map_id in gene_ids:
            key = (map_id, taxon_id)

            try:
                newcounts[key] += count
            except KeyError:
                newcounts[key] = count

    return pd.Series(newcounts)
