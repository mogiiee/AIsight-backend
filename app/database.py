from . import exporter
import pymongo


cluster = pymongo.MongoClient("mongodb://amogh:amogh@ac-ztxn30c-shard-00-00.esico7b.mongodb.net:27017,ac-ztxn30c-shard-00-01.esico7b.mongodb.net:27017,ac-ztxn30c-shard-00-02.esico7b.mongodb.net:27017/?ssl=true&replicaSet=atlas-i1fgx7-shard-0&authSource=admin&retryWrites=true&w=majority")

db = cluster[exporter.db_name]

user_collection = db[exporter.full_collection]

