from __future__ import division, unicode_literals, print_function

from matgendb.query_engine import QueryEngine

qe = QueryEngine(host="10.5.46.101", port=27017,
                 database="vasp", collection="NIST",
                 user="km468", password="km468")
# the following query works only if any of the documents contain
# the hkl field
results = list( qe.query(criteria={"pretty_formula": "H4C"},
                         properties=['author','energy',
                                     'cif', 'pretty_formula',
                                     'volume']) )

print('formula : {}'.format(results[0]['pretty_formula']))
print('author : {}'.format(results[0]['author']))
print('ligand : {}'.format(results[0]['ligand']))
print('energy : {}'.format(results[0]['energy']))
#print('CIF structure data = \n {}'.format(results[0]['cif']))
print(results[0]['volume'])

