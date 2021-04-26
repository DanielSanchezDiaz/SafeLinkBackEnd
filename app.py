from flask_cors import CORS
import checks_hub
from flask import Flask
from flask import request

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
    url = request.json['domain_name']
    results = checks_hub.main_security(url)
    # CONVERT TO NECESSARY FORMAT AND RETURN AS RESPONSE TO API CALL
    return results


if __name__ == '__main__':
    app.run()
