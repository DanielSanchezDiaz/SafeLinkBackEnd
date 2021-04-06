import ssl
import urllib

import certifi
from flask import Flask
from flask_pymongo import pymongo


client = pymongo.MongoClient(
    "mongodb+srv://DanielSanchez:SafeLink123@topdomainnames.mj0ts.mongodb.net/DomainNames?retryWrites=true&w=majority",
    )
db = client.test
client.server_info()
#user_collection = pymongo.collection.Collection(db, 'user_collection')
