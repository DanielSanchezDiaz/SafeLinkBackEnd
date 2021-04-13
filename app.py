
from algorithms.combosquatting.combosquatting import find_combosquatting
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from generateTypo import ts_models
from requests import request
import tldextract

app = Flask(__name__)
cors = CORS(app)

import db


@app.cli.command()
def updateDataBase():
    """Gets top domains from tranco and updates the db with typos and top domain names"""
    db.upDateDataBase()
    print("Updated Data base!")


@app.route("/processLink", methods=['GET', 'POST'])
def processLink():
    object = {
        "passed": False,
        "typoArr": [],
        "comboArr": []
    }
    typoModel = ts_models()
    typos = typoModel.generate_ts_domains("google.com")
    print(typos.values())
    links = request.json
    firstLink = links[0].lower()
    parts = tldextract.extract(firstLink)
    cl_domain = [parts.domain, '.' + parts.suffix]
    f_clean_domain = ''.join(cl_domain)
    result = db.queryTypoSquat(f_clean_domain)
    if result:
        return jsonify(object)
    else:
        return jsonify("Coast is clear!")


if __name__ == '__main__':
    app.run()
