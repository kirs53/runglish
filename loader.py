from elasticsearch import Elasticsearch
import csv

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
print(f"Connected to ElasticSearch cluster {es.info().body['cluster_name']}")

with open("./data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        document = {
            "word": row["word"],
            "form": row["form"],
            "sentence": row["sentence"],
            "paraphrase": row["paraphrase"]
        }
        es.index(index="word_index", document=document)
