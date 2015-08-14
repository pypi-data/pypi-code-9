# -*- coding: utf-8 -*-
import csv
import urllib2
import operator


def read_sif(file_url):
    """
    Read a SIF network file and create triples as a list

    :param file_url: Location of the input SIF file
    :return: list of strings (source, interaction, target)
    """
    triples = []
    reader = csv.reader(urllib2.urlopen(file_url), delimiter='\t')

    for line in reader:
        triples.append(line)

    return triples


def filter_sif(triples, scores, desired_nodes=30):
    scores_made_the_cut = sorted(
        scores.items(),
        key=operator.itemgetter(1),
        reverse=True)[0:(desired_nodes)]

    nodes_made_the_cut = [i[0] for i in scores_made_the_cut]
    edges_made_the_cut = []

    for tr in triples:
        if (tr[0] in nodes_made_the_cut) and (tr[2] in nodes_made_the_cut):
            edges_made_the_cut.append(tr)

    return edges_made_the_cut


def sif2cx(triples, scores=None):
    cx_out = []
    identifier_to_node_id_map = {}
    id_counter = 1000

    for tr in triples:
        subj_node_id = identifier_to_node_id_map.get(tr[0])
        obj_node_id = identifier_to_node_id_map.get(tr[2])

        if not subj_node_id:
            subj_node_id = "_" + str(id_counter)
            id_counter = id_counter + 1
            identifier_to_node_id_map[tr[0]] = subj_node_id
            cx_out.append({"nodes": [{"@id": subj_node_id}]})
            cx_out.append({"nodeIdentities": [{"node": subj_node_id, "represents": tr[0]}]})

        if not obj_node_id:
            obj_node_id = "_" + str(id_counter)
            id_counter = id_counter + 1
            identifier_to_node_id_map[tr[2]] = obj_node_id
            cx_out.append({"nodes": [{"@id": obj_node_id}]})
            cx_out.append({"nodeIdentities": [{"node": obj_node_id, "represents": tr[2]}]})

        edge_section = {
            "edges": [
                {
                    "source": subj_node_id, "@id": "_" + str(id_counter),
                    "target": obj_node_id
                }
            ],
            "edgeIdentities": [
                {
                    "edge": "_" + str(id_counter),
                    "relationship": tr[1]
                }
            ]
        }
        cx_out.append(edge_section)
        id_counter = id_counter + 1

    if scores:
        for node_name, value in scores.iteritems():
            node_id = identifier_to_node_id_map.get(node_name)
            if node_id:
                node_section = {
                    "elementProperties": [
                        {
                            "node": node_id,
                            "property": "subnet_finder_score",
                            "value": value
                        }
                    ]
                }
                cx_out.append(node_section)

    return cx_out


def query_vector(query, labels):
    out = {}
    weight_sum = 0.0
    for i in labels:
        if i in query:
            out[i] = 1.0
            weight_sum += 1.0
        else:
            out[i] = 0.0

    for i in labels:
        out[i] = out[i] / weight_sum

    return out
