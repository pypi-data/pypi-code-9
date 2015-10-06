import time
import os
import json

from bioservices import KEGG
from easydev import Progress, Logging


class KEGGReader(Logging):
    def __init__(self, organism='hsa', verbose=True):
        super(KEGGReader, self).__init__(level=verbose)

        self.nodes1 = []
        self.nodes2 = []
        self.edges = []
        self.organism = organism
        self.edges = []
        self.pathways = []
        self.links = []
        self.names = []
        self.gene_names = {}

    def build_whole_graph(self, verbose=False, cache=True):
        self.kegg = KEGG(verbose=verbose, cache=True)
        self.kegg.organism = self.organism
        pb = Progress(len(self.kegg.pathwayIds))
        for i, eid in enumerate(self.kegg.pathwayIds):
            if os.path.isfile(eid + ".json"):
                kgml = json.loads(open(eid + ".json", "r").read())
            else:
                kgml = self.kegg.parse_kgml_pathway(eid)
                fh = open(eid+".json", "w")
                fh.write(json.dumps(kgml))
                fh.close()
                res = self.interpret_kgml(kgml, eid)
                pb.animate(i)
                self._cleanup()

    def _cleanup(self):
        # in rare occasion, there is a special character to get rid of
        # over hsa, this convert 1 entry that is written: hsa:xxxx\uff0bmmu:YYYY
        self.nodes1 = [x.split(u"\uff0b")[0] for x in self.nodes1]
        self.nodes2 = [x.split(u"\uff0b")[0] for x in self.nodes2]

    def _filter_entries(self, kgml):
        entries = kgml['entries']
        # filter to keep only genes
        entries = [x for x in entries if x['type'] == "gene"]
        self.info("Keeping %s gene entries out of %s" %
             (len(entries),len(kgml['entries'])))
        return entries
    def _filter_relations(self, kgml):
        relations = kgml['relations']
        N1 = len(relations)
        relations = [x for x in relations if x['value'] in ["-->", "--|"]]
        N2 = len(relations)
        self.info("Keeping %s relations with activation or inhibition (out of %s)"
             % (N2, N1))
        return relations

    def interpret_kgml(self, kgml, eid):
        """Interpret a KGML file to populate the attributes with found relations
        :attr:`nodes1`, :attr:`nodes2` and :attr:`edges`
        """
        # keep only gene names and relations of interest that is those
        # represented as --> and --|
        entries = self._filter_entries(kgml)
        relations = self._filter_relations(kgml)
        self.skipped = 0
        for r in relations:
            entry1 = [x for x in entries if x['id'] == r['entry1']]
            if len(entry1) == 0:
                continue
            entry1 = entry1[0]
            entry2 = [x for x in entries if x['id'] == r['entry2']]
            if len(entry2) == 0:
                continue
            entry2 = entry2[0]
            name = r['name']
            link = r['link']
            value = r['value']

            if value == "-->":
                for x in entry1['name'].split(" "):
                    for y in entry2['name'].split(" "):
                        self.nodes1.append(x)
                        self.nodes2.append(y)
                        self.edges.append("+")
                        self.pathways.append(eid)
                        self.links.append(link) # link name e.g., PPrel
                        self.names.append(name) # another link name e.g., activation
                        self.gene_names[x] = entry1['gene_names']
                        self.gene_names[y] = entry2['gene_names']
            elif value == "--|":
                for x in entry1['name'].split(" "):
                    for y in entry2['name'].split(" "):
                        self.nodes1.append(x)
                        self.nodes2.append(y)
                        self.edges.append("-")
                        self.pathways.append(eid)
                        self.links.append(link) # link name e.g., PPrel
                        self.names.append(name) # another link name e.g., activation
                        self.gene_names[x] = entry1['gene_names']
                        self.gene_names[y] = entry2['gene_names']
            else:
                self.skipped += 1
        self.info("Skipped %s relations and kept %s" % (self.skipped, len(relations)-self.skipped))





class KGML(object):
    def __init__(self, data):
        if isinstance(str):
            # could be a file or data
            self.from_json(self, data)

    def from_json(self, filename):
        data = open(filename, 'r').read()
        data = json.loads(data)
        self.data = data
        
