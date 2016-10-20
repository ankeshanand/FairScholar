from math import sqrt
import matplotlib.pyplot as plt
import json
import pygraphviz as pgv
__author__ = 'ankesh'
import networkx as nx
import community

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
del keydict

#a = nx.to_agraph(g)
#print "Converted the graph to AGraph."
#a.write("file.dot")

#nx.draw(g)
#plt.savefig("keyword-graph.png")

print "Community Detection started"
#first compute the best partition
partition = community.best_partition(g)
print "computed best partition"
print "Louvain Modularity: ", community.modularity(partition, g)
#drawing
size = float(len(set(partition.values())))
print "The size is "+str(size)
#pos = nx.spring_layout(g)
#print "Generated Spring Layout"
count = 0.
# comlist = []
# for com in set(partition.values()):
#     count = count + 1.
#     list_nodes = [nodes for nodes in partition.keys()
#                                 if partition[nodes] == com]
#     comlist.append(list_nodes)
# print "Finished generating communities"
#
# with open('commlist.json', 'w') as outfile:
#     json.dump(comlist, outfile)

commdict = {}
for elem, part in partition.items():
    commdict[elem] = part
            #f.write(str(elem) + " " + str(part) + "\n")
print "There are "+str(len(commdict))+" keys in the keyword community dictionary."
with open('../data/keyword-community-dict.json', 'w') as outfile:
    json.dump(commdict, outfile)
#nx.draw_networkx_edges(g, pos, alpha=0.5)
#print "Finished drawing networkx edges"
#plt.show()
