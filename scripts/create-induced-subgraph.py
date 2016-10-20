__author__ = 'ankesh'
import json
import networkx as nx

commdict = {}
with open("../data/keyword-community-dict.json", 'r') as f:
    commdict = json.load(f)
print "Loaded keyword community dictionary."

comm_keylist_dict = {}
for keyword in commdict:
    community = commdict[keyword]
    if community not in comm_keylist_dict:
        comm_keylist_dict[community] = []
    comm_keylist_dict[community].append(keyword)

print "Created a list of keywords for each Community."

del commdict
keypaperdict = {}
with open("../data/keyword-paper-dict.json", 'r') as f:
    keypaperdict = json.load(f)
print "Loaded Keyword Paper dictionary."

g = nx.DiGraph()
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
toppapers_dict = {}
for comm in comm_keylist_dict:
    "Starting computation for community "+str(comm)
    paperlist = []
    for keyword in comm_keylist_dict[comm]:
        for paperid in keypaperdict[keyword]:
            paperlist.append(paperid)
    print "Created Paperlist for all keywords in community "+str(comm)

    induced = g.subgraph(paperlist)
    print "Created Induced Graph for "+str(comm)
    print "The number of nodes in the induced subgraph is "+str(nx.number_of_nodes(induced))

    total_incitations = 0.0

    for n in induced.nodes_iter():
        total_incitations += induced.in_degree(n)

    print total_incitations

    for n in induced.nodes_iter():
        induced.node[n]['pstar'] = induced.in_degree(n) / (total_incitations*1.0)
        induced.node[n]['pt'] = 1.0 / (induced.number_of_nodes())
    print "Finished computing pstar and pt for "+str(comm)

    for e in induced.edges_iter():
        x = e[0]
        y = e[1]
        if x == y:
            induced.edge[x][y]['pzero'] = 1.0 - 0.25
        else:
            induced.edge[x][y]['pzero'] = 0.25 * 1.0 / induced.in_degree(x)
        induced.edge[x][y]['p'] = induced.edge[x][y]['pzero']

    print "Finished computing pzero for "+str(comm)
    tsum_prev = 0.0
    for t in range(1, 100):
        for n in induced.nodes_iter():
            pcurr = 0.0
            for u, v in induced.edges(n):
                if v == n:
                    pcurr += induced.edge[u][v]['p'] * induced.node[n]['pt']
            induced.node[n]['ptnew'] = pcurr
        for n in induced.nodes_iter():
            induced.node[n]['pt'] = induced.node[n]['ptnew']
        for n in induced.nodes_iter():
            dcurr = 1.0
            for u, v in induced.edges(n):
                if u == n:
                    dcurr += induced.edge[u][v]['pzero'] * induced.node[v]['pt']
            induced.node[n]['dt'] = dcurr
        for e in induced.edges_iter():
            u = e[0]
            v = e[1]
            induced.edge[u][v]['p'] = 0.5*induced.node[v]['pstar'] + \
                0.5*(induced.edge[u][v]['pzero'] * induced.node[v]['pt'] / induced.node[u]['dt'])
        print
        tsum = 0.0
        for n in induced.nodes_iter():
            tsum += 1000000.0 * induced.node[n]['pt']
        if abs(tsum - tsum_prev) < 0.0001:
            toppapers_dict[comm] = []
            npapers = 0
            for u, dct in sorted(induced.nodes(data=True), key=lambda (u, dct): dct['pt']):
                toppapers_dict[comm].append([u, induced.node[u]['pt']])
                npapers += 1
            print len(toppapers_dict[comm])
            print "Finished computation for community "+str(comm)
            break
        tsum_prev = tsum
        print "t= "+str(t)+" sum= "+str(tsum)+" for community "+str(comm)

with open('../data/top-papers-dict.json', 'w') as outfile:
    json.dump(toppapers_dict, outfile)

