import json
__author__ = 'ankesh'
import networkx as nx

g = nx.Graph()

keyhashes = []
keydict = {}
edgeshash = set([])

keylists = []
with open('../data/keyword-edges-dict.json', 'r') as f:
    keydict = json.load(f)

print "Finished loading Dict."
print "Size of dict is "+str(len(keydict))
count = 0
for mainkey in keydict:
    for secondkey in keydict[mainkey]:
        g.add_edge(mainkey, secondkey, weight=keydict[mainkey][secondkey])
    if count % 100 == 0:
        print "Processed "+str(count)+" keys."
    count += 1

print "Finished computing graph."
nx.write_pajek(g, '../data/citation-graph.net')
del keydict