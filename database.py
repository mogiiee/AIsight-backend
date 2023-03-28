import exporter
import pymongo


cluster = pymongo.MongoClient(exporter.cluster)

db = cluster[exporter.dbase]

user_collection = db[exporter.collection]

