__author__ = 'ankesh'
import json
import networkx as nx

g = nx.Graph()
count = 0
paperidx = 0
keypaperdict = {}
with open("../data/combined") as f:
    for line in f:
        if line.startswith('#index'):
            paperidx = int(line[6:])
            #print paperidx
            count += 1
            if count % 10000 == 0:
                print "Processed "+str(count)+" papers."

        if line.startswith('#K'):
            endidx = line.find('[')
            word = line[2:endidx]
            if word not in keypaperdict:
                keypaperdict[word] = []
            keypaperdict[word].append(paperidx)

print "Finished processing all papers."
with open('../data/keyword-paper-dict.json', 'w') as outfile:
    json.dump(keypaperdict, outfile)