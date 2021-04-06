import ssl
import urllib

import certifi
from flask import Flask
from flask_pymongo import pymongo
from app import app
from generateTypo import ts_models
from tranco import Tranco

client = pymongo.MongoClient(
    "mongodb+srv://DanielSanchez:SafeLink@topdomainnames.mj0ts.mongodb.net/DomainNames?retryWrites=true&w=majority",
    ssl=True, ssl_cert_reqs='CERT_NONE')
db = client.get_database('DomainNames')


def getTopDomains():
    '''Returns a list of the top domains'''
    t = Tranco(cache=True, cache_dir='.tranco')
    latest_list = t.list().top(10000)
    return latest_list


def upDateDataBase():
    topDomainsCol = db.get_collection('TopDomainNames')
    domains = getTopDomains()
    i = 0
    typoCol = db.get_collection('TypoSquats')
    typoModel = ts_models()
    typoId = 1
    for domain in domains:
        entry = {"_id": str(i), "domain": domain}
        topDomainsCol.save(entry)
        # Save the typos ***************
        typos = typoModel.generate_ts_domains(domain)
        for typ in typos:
            for typo in typ:
                entry = {"_id": str(typoId), "typo": typo, "domain": domain}
                typoCol.save(entry)
                typoId += 1
        # *******************************
        i += 1


def queryTypoSquat(link):
    typoCol = db.get_collection('TypoSquats')
    result = typoCol.find_one({'typo': link})
    return result