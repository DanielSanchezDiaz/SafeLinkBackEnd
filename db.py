import ssl
import urllib

import certifi
from flask import Flask
from flask_pymongo import pymongo
from app import app

client = pymongo.MongoClient(
    "mongodb+srv://<nice try>:<nope>@topdomainnames.mj0ts.mongodb.net/DomainNames?retryWrites=true&w=majority",
    ssl=True, ssl_cert_reqs='CERT_NONE')
db = client.get_database('DomainNames')
domainNames = db.get_collection('TopDomainNames')
results = domainNames.find()
# for doc in results:
#     print(doc)
