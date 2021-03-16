import ssl
import urllib

import certifi
from flask import Flask
from flask_pymongo import pymongo
from app import app

client = pymongo.MongoClient(
    "mongodb+srv://TestUser:FakePassword@cluster0.uttgb.mongodb.net/Test-Database?retryWrites=true&w=majority",
    ssl=True, ssl_cert_reqs='CERT_NONE')
db = client.get_database('Test-Database')
user_collection = pymongo.collection.Collection(db, 'user_collection')
