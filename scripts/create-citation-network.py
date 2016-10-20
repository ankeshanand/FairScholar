__author__ = 'ankesh'
import json
import networkx as nx

g = nx.Graph()
count = 0
with open("../data/combined") as f:
    for line in f:
        if line.startswith('#index'):
            paperidx = int(line[6:])
            #print paperidx
            g.add_edge(paperidx, paperidx)
            count += 1
            if count % 10000 == 0:
                print "Processed "+str(count)+" papers."

        if line.startswith('#%*'):
            start = line.find('[')
            end = line.find(']')
            if line[start+1:end].isdigit():
                refpaperidx = int(line[start+1:end])
                g.add_edge(paperidx, refpaperidx)

print "Finished processing all papers."
nx.write_graphml(g, "../data/citation-graph.graphml")