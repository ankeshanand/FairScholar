from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import json
from fairscholar.models import Keywords, Papers
from random import shuffle
import re
# Create your views here.


def get_keyword(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        keylist = q.strip().split(',')
        q = keylist[-1]
        keywords = Keywords.objects.filter(keyword__icontains = q)[:20]
        results = []
        for keyword in keywords:
            keyword_json = {}
            keyword_json['id'] = keyword.id
            keyword_json['label'] = keyword.keyword
            keyword_json['value'] = keyword.keyword
            results.append(keyword_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def show_results(request):
    papers_list = []
    community = -1
    keywords = request.GET.get('keyword')
    paperdict = {}
    keyword_list = keywords.split(',')
    search_terms = ''
    nkeywords = 0
    regex = re.compile('\[.+?\]')
    for keyword in keyword_list:
        keyword = keyword.strip()
        query_term = "\""+keyword+"\""
        keyword_term = '%% '+keyword+' %%'
        if Keywords.objects.filter(keyword__iexact=keyword).exists():
            nkeywords += 1
            if not search_terms:
                search_terms += keyword
            else:
                search_terms += " and " + keyword
            community = Keywords.objects.filter(keyword__iexact=keyword)[0].community
        if community != -1:
           #  print "keyword_term="+keyword_term
           # print query_term
            query = Papers.objects.raw("""
                      SELECT * from papers  WHERE ((community = %s) AND (MATCH(name, summary) AGAINST(%s IN BOOLEAN MODE))) order by score desc limit 10""", [community, query_term])
            for paper in query:
                paperdict = {'index': paper.paperid,
                             'name': paper.name.title(),
                             'authors': regex.sub('', paper.authors)[:-1],
                             'summary': paper.summary[:400] + '..' if len(paper.summary) > 100 else paper.summary,
                             'year': paper.year,
                             'link': 'http://libra.msra.cn/Publication/'+str(paper.paperid)}
                papers_list.append(paperdict)
           # print "The number of papers are"+str(len(papers_list))
            if len(papers_list) < 10:
            #    print "Less than 10."
                papers_list = []
                for paper in Papers.objects.raw("""
                      SELECT * from papers  WHERE (MATCH(name, summary) AGAINST(%s IN BOOLEAN MODE)) order by score desc limit 100""", [query_term]):
                    paperdict = {'index': paper.paperid,
                             'name': paper.name.title(),
                             'authors': regex.sub('', paper.authors)[:-1],
                             'summary': paper.summary[:400] + '..' if len(paper.summary) > 100 else paper.summary,
                             'year': paper.year,
                             'link': 'http://libra.msra.cn/Publication/'+str(paper.paperid)}
                    papers_list.append(paperdict)

        #Look for keyword in the title and summary if there are are no matching entries in the keywords table.
        else:
            search_terms += keyword
           #  print query_term
            for paper in Papers.objects.raw("""
                      SELECT * from papers  WHERE (MATCH(name, summary) AGAINST(%s IN BOOLEAN MODE)) order by score desc limit 100""", [query_term]):
                paperdict = {'index': paper.paperid,
                             'name': paper.name.title(),
                             'authors': regex.sub('', paper.authors)[:-1],
                             'summary': paper.summary[:400] + '..' if len(paper.summary) > 100 else paper.summary,
                             'year': paper.year,
                             'link': 'http://libra.msra.cn/Publication/'+str(paper.paperid)}
                papers_list.append(paperdict)
           #  print "The number of papers are:"+str(len(papers_list))
        community = -1
    if nkeywords > 1:
        # print "The number of keywords are greater than 1."
        shuffle(papers_list)
    return render(request, 'results.html', {'papers_list': papers_list, 'keyword': search_terms})


