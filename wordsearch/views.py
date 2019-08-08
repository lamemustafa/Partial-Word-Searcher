from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from elasticsearch import Elasticsearch
import json
import logging
import traceback

#Connection to ElasticSearch server.
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#home page with a search box to search keywords
def home(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
    return render(request,'wordsearch/index.html')

#method for doing partial searches using query language
@csrf_exempt
def partial_search(request):
    try:
        if request.method == "GET":

            # if query parameter word not in url
            if 'word' not in request.GET:
                return HttpResponseNotFound('<h1>Page Not Found</h1>') 

            #if query parameter word in url
            word=request.GET.get('word')
            keyWord = str('*'+word+'*')

            #query to search index
            q1={
                    'bool':{
                        'should':[
                            {
                                'term':{
                                    'word':word
                                }
                            },
                            {
                                'query_string':{
                                    'query':keyWord,
                                    'fields':['word',]
                                }
                            },
                        ]
                    }
            }

            #search in index
            t = es.search(index=["word_list"],body={"from":0,"size":10000,"query":q1})
  
            #getting data from index
            temp_word = {}
            for k in t['hits']['hits']:
                words = k['_source']['word']
                score = k['_source']['usage_frequency']
                temp_dict = {words:score}
                if temp_dict not in temp_word.items():
                    temp_word.update(temp_dict)
            
            #making list of usage frequency and sorting in descending order
            temp = []
            for k in temp_word:
                temp.append(temp_word[k])
            temp.sort(reverse=True)

            #making a new list of words according to thier usage frequecy
            temp1 =[]
            for i in temp:
                for k in temp_word:
                    if i == temp_word[k]:
                        temp1.append(k)
            
            #swapping the position of word searched with first element of list
            for i in range(0,len(temp1)):
                if word == temp1[i]:
                    a=temp1[0]
                    temp1[0]=temp1[i]
                    temp1[i]=a
                    break
            
            #getting top 25 values from list and sorting them according to thier length
            temp1=sorted(temp1[:25],key=len)

            return JsonResponse({'data':temp1})
            #return JsonResponse(temp1,safe=False)

    except Exception as e:
        logging.error("Exception Occured during login",exc_info=True)
        traceback.print_exc()
        return JsonResponse({'Error':'BadRequest'})
