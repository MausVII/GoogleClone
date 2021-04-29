from django.shortcuts import render
import csv
import requests
import os, pathlib
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(hosts=["localhost:9200"])

# Create your views here.
def index(request):
    load_data()
    return render(request, 'index.html')

def search(request):
    print(es.indices.get_alias("*"))
        
    return render(request, 'search.html')

def load_data():
    with open ("search/lyrics.csv", 'r') as file:
        reader = csv.DictReader(file)
        helpers.bulk(es, reader, index="index_name")
        
    

    