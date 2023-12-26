from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
import csv

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

with open("./data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        document = {
            "word": row["word"],
            "form": row["form"],
            "sentence": row["sentence"],
            "paraphrase": row["paraphrase"]
        }
        es.index(index="runglishtorussian", document=document)

app = Flask(__name__)
MAX_SIZE = 20

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
    resp = es.search(index="runglishtorussian", body=payload, size=MAX_SIZE)
    return list({result['_source']['sentence']: result['_source']['paraphrase'] for result in resp['hits']['hits']}.items())
app.run(debug=True)