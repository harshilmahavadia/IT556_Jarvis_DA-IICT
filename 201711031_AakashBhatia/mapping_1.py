import csv
from elasticsearch import Elasticsearch

#mapping
mapping = {
    "music_map": {
        "properties": {
            "artist": {"type": "keyword", "index_options": "offsets"},
            "location": {"type": "keyword"},
            "similar": {"type": "keyword "},
            "song": {"type": "keyword"},
            "title": {"type": "integer"},
           
        }
    }
}

es = Elasticsearch()

if not es.indices.exists("music"):
    es.indices.create("music")
    es.indices.put_mapping(index="music",doc_type="music-map",body=mapping)

with open('music_new.csv') as csvfile:  #importing csv and index creation
    reader = csv.DictReader(csvfile)
    for row in reader:
        es.index(index="music", doc_type="music-map", body={"title": row['Title'], "song": row['song'], "similar": row['similar'],  "location": row['location'], "artist": row['artist']})

res = es.search(index="music", body={"query": {"match_all": {}}})

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(title)s %(song)s %(similar)s %(location)s %(artist)s" % hit["_source"])
