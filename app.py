from flask import Flask, request, jsonify
from flask_cors import CORS
from generateTypo import ts_models

app = Flask(__name__)
cors = CORS(app)

import db


# test to insert data to the data base
@app.route("/test")
def test():
    db.db.TestDatabase.insert_one({"name": "John"})
    return "Connected to the data base!"


@app.route("/frontend")
def connect():
    return {
        'son': 'Obed'
    }


@app.route("/processLink", methods=['GET', 'POST'])
def processLink():
    print("hi")
    links = request.json
    firstLink = links[0]
    typo = ts_models()
    potTypos = typo.generate_ts_domains(firstLink)
    print(firstLink)
    return jsonify(f"Potential Typo Squattings are {potTypos}")


if __name__ == '__main__':
    app.run()
