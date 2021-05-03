from algorithms.generateTypo import ts_models
from algorithms.generateCombo import find_combosquatting
from requests import request
from flask import jsonify
import tldextract
import db
import requests
import datetime
import copy
from algorithms.generateSound import Homophones


def typo_squatting(url, json_response_dict):
    """
    takes in a url and json object, generates a list of 
    possible typosquatted domains from the url and adds a key-value
    pair in the form {"typoSquatting": "[...]" }
    """

    result = db.queryTypoSquat(url)
    if result:
        json_response_dict["STATUS"] = "FAILED"
        result = [result['domain']]
    else:
        result = []
    json_response_dict["typoSquatting"] = result
    # ADD RESULT TO DICT HERE


def combo_squatting(url, json_response_dict):
    """
    takes in a url and json object, generates a list of 
    possible combosquatted domains from the url and adds a key-value
    pair in the form {"comboSquatting": "[...]" }
    """
    combo_list = find_combosquatting(url)
    if combo_list:
        json_response_dict["STATUS"] = "FAILED"
    json_response_dict["comboSquatting"] = combo_list
    # add to dict


def sound_squatting(url, json_response_dict):
    """
    takes in a url and json object, generates a list of
    possible soundsquatted domains from the url and adds a key-value
    pair in the form {"comboSquatting": "[...]" }
    """
    result = db.querySoundSquat(url)
    if result:
        json_response_dict["STATUS"] = "FAILED"
        result = [result['domain']]
    else:
        result = []
    json_response_dict["soundSquatting"] = result


def homograph_squatting(url, json_response_dict):
    # add check to see if url starts with xn-- (that's punycode)
    # u"ẙ𑣎ụťụhѳ.com".encode("idna")
    print("The clean domain is: "+url)
    result = db.queryHomoSquat(url)
    if result:
        json_response_dict["STATUS"] = "FAILED"
        result = [result['domain']]
    else:
        result = []
    json_response_dict["homographSquatting"] = result


def detect_new_domains(url, json_response_dict):
    info = requests.get("https://www.rdap.net/domain/"+url)
    if info.status_code == 400:
        json_response_dict['STATUS'] = 'FAILED'
        json_response_dict['New Domain'] = ["rdap was unable to find information on this domain"]
        json_response_dict['expiration'] = []
        json_response_dict['registration'] = []
        return

    info = info.json()
    events = info["events"]
    response = []
    numDays = 30
    for event in events:
        if event['eventAction'] == 'expiration':
            json_response_dict['expiration'] = [event['eventDate']]
        if event['eventAction'] == 'registration':
            date = event['eventDate']
            json_response_dict['registration'] = [date]
            day, time = date.split('T')
            year, month, day = day.split('-')
            registrationDate = datetime.date(int(year), int(month), int(day))
            currentDate = datetime.datetime.date(datetime.datetime.now())
            diff = currentDate - registrationDate
            # one month is reasonable
            # make days a parameter
            if diff.days < numDays:
                json_response_dict['STATUS'] = 'FAILED'
                response = f"This domain was registered {diff.days} ago" #display something with this on frontend
    json_response_dict['New Domain'] = [response]


url_cache = {}


def main_security(url):
    """
    takes a url and passes the url to different
    modules each checking for different
    security threats and returns the result as a json object 
    with key value pairs as follows:

        {
            STATUS: <FAILED>,
            "comboSquatting": "[...]",
            "typoSquatting": "[...],
            "soundSquatting": "[...],
            "homographSquatting": [...],
            "New Domain": "[...]"
            ...
        }
    """

    json_response_dict = {
        "STATUS": "PASSED"
    }
    parts = tldextract.extract(url)
    cl_domain = [parts.domain, '.' + parts.suffix]
    url = ''.join(cl_domain)

    # handle puny code
    if url.startswith("xn--"):
        url = url.encode("utf-8").decode("idna")
    if url in url_cache:
        print(url_cache[url])
        return url_cache[url]
    typo_squatting(url, json_response_dict)
    combo_squatting(url, json_response_dict)
    sound_squatting(url, json_response_dict)
    homograph_squatting(url, json_response_dict)
    detect_new_domains(url, json_response_dict)
    url_cache[url] = copy.deepcopy(json_response_dict)
    print(json_response_dict)
    return json_response_dict
