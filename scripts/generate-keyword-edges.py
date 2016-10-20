__author__ = 'ankesh'
import json
keylists = []
templist = []
keydict = {}
with open("../data/combined") as f:
    for line in f:
        if line.startswith('#index'):
            for firstkey in templist:
                if firstkey not in keydict:
                    keydict[firstkey] = {}
                for secondkey in templist:
                    if secondkey != firstkey:
                        if secondkey in keydict[firstkey]:
                            keydict[firstkey][secondkey] += 1
                        else:
                            keydict[firstkey][secondkey] = 1
            templist = []
        if line.startswith('#K'):
            endidx = line.find('[')
            word = line[2:endidx]
            #print word
            templist.append(word)

for mainkey in keydict:
    for secondkey in keydict[mainkey].keys():
        if keydict[mainkey][secondkey] <= 2:
            del keydict[mainkey][secondkey]
print "There are "+str(len(keydict))+" keys in the dictionary."
with open('../data/keyword-edges-dict.json', 'w') as outfile:
    json.dump(keydict, outfile)