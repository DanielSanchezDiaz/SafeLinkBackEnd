from flask_pymongo import pymongo
from algorithms.generateTypo import ts_models
from algorithms.generateSound import Homophones
from tranco import Tranco

client = pymongo.MongoClient(
    "mongodb+srv://DanielSanchez:SafeLink@topdomainnames.mj0ts.mongodb.net/DomainNames?retryWrites=true&w=majority",
    ssl=True, ssl_cert_reqs='CERT_NONE')
db = client.get_database('DomainNames')


def getTopDomains():
    '''Returns a list of the top domains'''
    t = Tranco(cache=False, cache_dir='.tranco')
    latest_list = t.list().top(10000)
    return latest_list


def upDateDataBase():
    topDomainsCol = db.get_collection('TopDomainNames')
    domains = getTopDomains()
    i = 1
    typoCol = db.get_collection('TypoSquats')
    soundcol = db.get_collection('SoundSquats')
    typoModel = ts_models()
    homoModel = Homophones('file_database/homophone_list', 'file_database/wordlists/wordsEn.txt')
    typoId = 1
    homoId = 1
    for domain in domains:
        entry = {"_id": str(i), "domain": domain}
        topDomainsCol.save(entry)
        # Save the typos ***************
        typos = typoModel.generate_ts_domains(domain)
        for typ in typos:
            for typo in typos[typ]:
                entry = {"_id": str(typoId), "typo": typo, "domain": domain}
                typoCol.save(entry)
                typoId += 1
        # *******************************
        homos = homoModel.find_h_domains_single(domain)
        for squat in homos["soudsquatting_single"]:
            entry = {"_id": str(homoId), "squat": squat[0], "domain": domain}
            soundcol.save(entry)
            homoId += 1
        for squat in homos["soudsquatting_double"]:
            entry = {"_id": str(homoId), "squat": squat[0], "domain": domain}
            soundcol.save(entry)
            homoId += 1
        i += 1


def queryTypoSquat(link):
    typoCol = db.get_collection('TypoSquats')
    result = typoCol.find_one({'typo': link})
    return result


def getAllDomains():
    topDomainsCol = db.get_collection('TopDomainNames')
    return list(topDomainsCol.find({}))


def querySoundSquat(link):
    soundCol = db.get_collection('SoundSquats')
    result = soundCol.find_one({'squat': link})
    return result
