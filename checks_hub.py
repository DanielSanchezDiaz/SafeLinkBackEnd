from algorithms.generateTypo import ts_models
from algorithms.generateCombo import find_combosquatting
from requests import request
from flask import jsonify
import tldextract
import db




def typo_squatting(url, json_response_dict):
    """
    takes in a url and json object, generates a list of 
    possible typosquatted domains from the url and adds a key-value
    pair in the form {"typoSquatting": "[...]" }
    """
    typoModel = ts_models()
    typos = typoModel.generate_ts_domains("google.com")
    print(typos.values())
    links = request.json
    firstLink = links[0].lower()
    parts = tldextract.extract(firstLink)
    cl_domain = [parts.domain, '.' + parts.suffix]
    f_clean_domain = ''.join(cl_domain)
    result = db.queryTypoSquat(f_clean_domain)

    # if result:
    #     return jsonify("Typosquat detected!")
    # else:
    #     return jsonify("Coast is clear!")

    # ADD RESULT TO DICT HERE

def combo_squatting(url, json_response_dict):
    """
    takes in a url and json object, generates a list of 
    possible combosquatted domains from the url and adds a key-value
    pair in the form {"comboSquatting": "[...]" }
    """
    combo_list = find_combosquatting(url)
    # add to dict





def main_security_check_module(url):
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
    return json_response_dict



