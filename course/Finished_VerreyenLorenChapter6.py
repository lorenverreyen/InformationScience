#!/usr/bin/env python
# coding: utf-8



#get_ipython().system('pip install whoosh')




import os

from whoosh import highlight
from whoosh.index import open_dir, create_in
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.qparser import QueryParser
from whoosh.query import *

from whoosh.lang.morph_en import variations



#create the schema

schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True),
                path=ID(stored=True))



#create the index

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)



#add the documents from the British corpus

OS_SEP = os.sep  # take care, different OS use different filepath separators!

writer = ix.writer()

for document in os.listdir("corpus_of_british_fiction"):
    with open("corpus_of_british_fiction" + OS_SEP + document, 'r') as text:
        writer.add_document(title=document, content=str(text.read()),
                            path=document)
writer.commit()


#parse query string

from whoosh import qparser, query

def parsequery(myinput):
    myquery = QueryParser("content", ix.schema, termclass=query.Variations).parse(myinput)
    return(myquery)
#!!!!!!



#Search the documents

def searchdocuments(myquery):
    with ix.searcher() as searcher:
        results = searcher.search(myquery, limit=None)
        # https://whoosh.readthedocs.io/en/latest/highlight.html#the-character-limit
        results.fragmenter.charlimit = None
        for hit in results: 
            print(hit.highlights("content", top=5))



if __name__ == "__main__" :
    myinput=""
    
    while not myinput == "q:":
        myinput=input("What are you looking for? press q: to quit.")
        if myinput=="q:": 
            print("The morphology tool has stopped!")
        else:
            print("your query is being processed!")
            myquery= parsequery(myinput)
            searchdocuments(myquery)
            
   

