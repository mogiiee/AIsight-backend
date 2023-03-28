import exporter
import pymongo


cluster = pymongo.MongoClient(exporter.cluster)

db = cluster[exporter.database]

user_collection = db[exporter.collection]

