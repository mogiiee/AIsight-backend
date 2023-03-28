from . import exporter
import pymongo


cluster = pymongo.MongoClient()

my_cluster = cluster(exporter.realcluster)

db = cluster[exporter.db_name]

user_collection = db[exporter.full_collection]

