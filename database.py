import exporter
import pymongo


cluster = pymongo.MongoClient(exporter.cluster)

db = cluster[exporter.db_name]

user_collection = db[exporter.collection]

