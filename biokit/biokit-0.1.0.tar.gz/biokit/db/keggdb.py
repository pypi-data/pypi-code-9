



class KEGGDB(object):
    def __init__(self):
        pass

    def mapping(self):
        # kegg mapping. This take a while to download
        self.kegg.TIMEOUT = 6000
        self.mapping_uniprot2kegg = self.kegg.conv("hsa", "uniprot")
        self.kegg.TIMEOUT = 30
        # 29889 uniprot keys but 18974 unique kegg identifier in values
        self.mapping_kegg2uniprot = dict([(v,k) for k,v in
            self.mapping_uniprot2kegg.items()])
        # !!!!! not unique but will do for now.
        # e.g., there are 2838 keys but 4250 uniprot identifiers from
        # mapping_uniprot
        # besides, uniprot mapping have 4215 unique identifiers.
        # There are 2970 unique KEGG identifiers in the list
        u = UniProt(cache=True)
        self.mapping_uniprot = u.mapping(fr="KEGG_ID", to="ID",
                query=str(" ".join(list(set(self.nodes1+self.nodes2)))))
        self.mapping_uniprot_hsa_up = dict((uni.split("_")[0], k)
                for k, values in self.mapping_uniprot.items()
                for uni in values)
