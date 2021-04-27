from algorithms.generateTypo import ts_models
from algorithms.generateCombo import find_combosquatting
from requests import request
from flask import jsonify
import tldextract
import db
import requests
import datetime
from algorithms.generateSound import Homophones


def typo_squatting(url, json_response_dict):
    """
    takes in a url and json object, generates a list of 
    possible typosquatted domains from the url and adds a key-value
    pair in the form {"typoSquatting": "[...]" }
    """
    parts = tldextract.extract(url)
    cl_domain = [parts.domain, '.' + parts.suffix]
    f_clean_domain = ''.join(cl_domain)
    result = db.queryTypoSquat(f_clean_domain)
    if result:
        json_response_dict["STATUS"] = "FAILED"
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
    parts = tldextract.extract(url)
    cl_domain = [parts.domain, '.' + parts.suffix]
    f_clean_domain = ''.join(cl_domain)
    result = db.querySoundSquat(f_clean_domain)
    if result:
        json_response_dict["STATUS"] = "FAILED"
    json_response_dict["soundSquatting"] = result


def homograph_squatting(url, json_response_dict):
    parts = tldextract.extract(url)
    cl_domain = [parts.domain, '.' + parts.suffix]
    f_clean_domain = ''.join(cl_domain)
    result = db.queryHomoSquat(f_clean_domain)
    if result:
        json_response_dict["STATUS"] = "FAILED"
    json_response_dict["homographSquatting"] = result


def detect_new_domains(url, json_response_dict):
    # Things to do
        # cache result of rdap query, with date you got it
        # check in database if you have record for this already

    parts = tldextract.extract(url)
    cl_domain = [parts.domain, '.' + parts.suffix]
    f_clean_domain = ''.join(cl_domain)
    info = requests.get("https://www.rdap.net/domain/"+f_clean_domain).json()
    # This should be the registration date
    events = info["events"]
    response = []
    numDays = 30
    for event in events:
        if event['eventAction'] == 'registration':
            date = event['eventDate']
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
    json_response_dict['New Domain'] = response


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
            ...
        }
    """

    json_response_dict = {
        "STATUS": "PASSED"
    }

    typo_squatting(url, json_response_dict)
    combo_squatting(url, json_response_dict)
    sound_squatting(url, json_response_dict)
    homograph_squatting(url, json_response_dict)
    detect_new_domains(url, json_response_dict)
    return json_response_dict
