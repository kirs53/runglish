from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
import csv

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
print(f"Connected to ElasticSearch cluster {es.info().body['cluster_name']}")


app = Flask(__name__)
MAX_SIZE = 10

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search_autocomplete():
    query = request.args["q"].lower()
    payload = {
        "query": {
            "match": {
                "word": {
                    "query": query,
                    "fuzziness": "AUTO"
                }
            }
        }
    }
    resp = es.search(index="word_index", body=payload, size=MAX_SIZE)
    return list({result['_source']['sentence']: result['_source']['paraphrase'] for result in resp['hits']['hits']}.items())


app.run(debug=True)
