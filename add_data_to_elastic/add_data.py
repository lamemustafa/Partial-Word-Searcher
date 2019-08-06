from elasticsearch import helpers,Elasticsearch
import pandas as pd
import json,sys

df = pd.read_csv('word_search.tsv',sep='\t')
# df = df.to_csv('words1',sep='\t')
# df = pd.read_csv('words1',sep='\t')
df.to_json('words',orient='records')

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

actions = []
with open('words','r') as json_file:
    body = json.load(json_file)
    for i in range(0,len(body)):
        actions.append({
            '_id':i,
            '_source':{
                'word':body[i].get('word'),
                'usage_frequency':body[i].get('usage_frequency'),
            }
        })
helpers.bulk(es, actions, index='word_list', doc_type='words')

# t = es.search(index="words_list",body={"from":0,"size":10,"query":{"match":{'word':'the'}}})
t = es.get(index='word_list',doc_type='words',id=0)
print(t)







