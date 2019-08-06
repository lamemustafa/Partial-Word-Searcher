from elasticsearch import helpers,Elasticsearch
import pandas as pd
import json,sys

# convert .tsv to JSON data
df = pd.read_csv('word_search.tsv',sep='\t')
df.to_json('words',orient='records')

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# bulk populate index with json data
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

# check item with id = 0 in index
t = es.get(index='word_list',doc_type='words',id=0)
print(t)







