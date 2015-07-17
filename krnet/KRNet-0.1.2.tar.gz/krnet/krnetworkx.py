#!/usr/bin/python
import os.path
import sys
import networkx as nx
from kreactions import KReactions
from networkx import DiGraph

class KRNetworkX(DiGraph):
	def __init__(self, fn=None):
		if fn==None:
			if sys.version_info.major >= 3:
				fn = input("Enter the KEGG Reaction file you want to load...\n")
			else:
				fn = raw_input("Enter the KEGG Reaction file you want to load...\n")
		kr = KReactions(fn)
		ur = kr.uniq_reactions()
		kr.set_reactions(ur)
		ed = []
		nd = []
		for i in range(len(kr)):
			for s in kr[i].substrates():
				ed.append((s,kr[i].id()))
				nd.append(s)
				nd.append(kr[i].id())
			for p in kr[i].products():
				ed.append((kr[i].id(),p))
				nd.append(kr[i].id())
				nd.append(p)
		ud =[nd[0]]
		for i in nd:
			if i not in ud:
				ud.append(i)
		DiGraph.__init__(self)
		DiGraph.add_nodes_from(self,ud)
		DiGraph.add_edges_from(self,ed)
	def write_to_file(self, fn=None):
		if fn==None:
			fn= "out_graph.gml"
		nx.write_gml(self,fn)
	
#MAIN
#kn = KRNetworkX("reaction_samples_orig.txt")
#kn.write_to_file()
#kn=nx.read_gml("out_graph.gml")
#print(kn.number_of_nodes())
#print(nx.load_centrality(kn))
