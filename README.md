# Partial-Word-Searcher
Django app using elasticsearch for partial keyword matching

### Features
- Partial word matching
- Endpoint for Fuzzy Search
- Matches can occur anywhere
- Common words are ranked higher
- Shorts words are ranked higher

### Using elasticsearch with python

To connect to elasticsearch:

`es = Elasticsearch([{'host': 'localhost', 'port': 9200}])`

Query For matching all words related to keyword:

`q1={'bool':{'should':[{'term':{'word':word}},{'query_string':{'query':keyWord,'fields':['word',]}},]}}`

Search in elastic index: 

`t = es.search(index=["word_list"],body={"from":0,"size":10000,"query":q1})`

