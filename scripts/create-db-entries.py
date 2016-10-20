__author__ = 'ankesh'
import json
import MySQLdb as mdb
import _mysql_exceptions
from settings_secret import *
import sys

#Set up the connection with database
conn = mdb.connect(host='localhost',
                            user=DB_USER,
                            passwd=DB_PASSWORD,
                            db='fairscholar_db')

#Set up a cursor to the database connection
cur = conn.cursor()

# Set up the keyword database table. It would tell which community a keyword lies in
# keyword_comm_dict = {}
# with open('../data/keyword-community-dict.json') as f:
#     keyword_comm_dict = json.load(f)
# for key in keyword_comm_dict:
#     try:
#         cur.execute("""INSERT INTO keywords (keyword,community) VALUES (%s, %s)""",
#                     (key, keyword_comm_dict[key]))
#
#     except _mysql_exceptions.ProgrammingError as (errno, strerror):
#             print("Error: Query error. \n {:d} \t {:s} for query".format(errno, strerror))
#
#     except _mysql_exceptions.IntegrityError as (errno, strerror):
#             print "Error: Query error. \n {:d} \t {:s}".format(errno, strerror)
# del keyword_comm_dict
# print "Built the keywords database table."

#Build a set of top-papers only
top_papers = set([])
top_papers_dict = {}
paper_scores = {}
papers_comm_dict = {}  # Map of top papers to community
with open('../data/top-papers-dict.json') as f:
    top_papers_dict = json.load(f)
for comm in top_papers_dict:
    for paperentry in top_papers_dict[comm]:
        papers_comm_dict[paperentry[0]] = comm
        top_papers.add(paperentry[0])
        paper_scores[paperentry[0]] = paperentry[1]
print "Built a set of top papers only. It contains "+str(len(top_papers))+" papers."

# Initialize a few values
paperidx = 0
pname = ''
pauthors = ''
psummary = ''
pyear = 1
count = 0

# Build the papers database table. Due to MySQL scaling issues, it contains only top papers for now.
with open("../data/combined") as f:
    for line in f:
        if line == '\n' and paperidx in top_papers:
            pcomm = papers_comm_dict[paperidx]
            try:
                cur.execute("""INSERT INTO papers (paperid, name, authors, summary, year, community, score)
                         VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE score=%s""",
                         (paperidx, pname, pauthors, psummary, pyear, pcomm, paper_scores[paperidx], paper_scores[paperidx]))
                count += 1
                if count % 100 == 0:
                    print "Processed "+str(count)+" papers."
                    conn.commit()

            except _mysql_exceptions.ProgrammingError as (errno, strerror):
                print("Error: Query error. \n {:d} \t {:s} for query".format(errno, strerror))

            except _mysql_exceptions.IntegrityError as (errno, strerror):
                print "Error: Query error. \n {:d} \t {:s}".format(errno, strerror)
        if line.startswith('#index'):
            paperidx = int(line[6:])
        if line.startswith('#y'):
            if line[2:-1].isdigit():
                pyear = int(line[2:-1])
            else:
                pyear = -1
        if line.startswith('#!'):
            psummary = line[2:-1]
        if line.startswith('#@'):
            pauthors = line[2:-1]
        if line.startswith('#*'):
            pname = line[2:-1]


