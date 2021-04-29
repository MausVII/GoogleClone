from django.shortcuts import render
import csv
import requests
import json
import os, pathlib
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(hosts=["localhost:9200"])

# Create your views here.
def index(request):
    load_data()
    return render(request, 'index.html')

def search(request):
    # entry = json.loads(request.POST['search'])
    entry = request.POST['search']

    query = {
        "query": {
            "match": {
                "name": entry
            }
        }
    }

    result = es.search(body=query)
    hits = result['hits']['hits']

    search_results = {
        'result_1' : {},
        'result_2' : {},
        'result_3' : {},
        'result_4' : {},
        'result_5' : {},
        'result_6' : {},
        'result_7' : {},
        'result_8' : {},
        'result_9' : {},
        'result_10' : {}
    }

    i = 1
    for hit in hits:
        song =  {
            "rank": hit.get('_source')['rank'],
            "name": hit.get('_source')['name'],
            "artist": hit.get('_source')['artist'],
            "year": hit.get('_source')['year'],
            "lyrics": hit.get('_source')['lyrics'],
        }
        search_results["result_{}".format(i)] = song
        i += 1

    print(search_results)

    for result in search_results:
        print("Song: ", search_results[result].get('name'), "\tArtist: ", search_results[result].get('artist'), "\tYear: ", search_results[result].get('year'))

    return render(request, 'search.html')

def load_data():
    with open ("search/lyrics.csv", 'r') as file:
        # "Rank","Song","Artist","Year","Lyrics","Source"
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i > 0 and i < 100:
                doc = {
                    'rank': row[0],
                    'name': row[1],
                    'artist': row[2],
                    'year': row[3],
                    'lyrics': row[4],
                }
                index_name = "index{}".format(i)
                es.index(index=index_name, id=i, body=doc)
            i += 1

        
    

    