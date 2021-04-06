from algorithms.combosquatting import find_combosquatting
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

# import db


# # test to insert data to the data base
# @app.route("/test")
# def test():
#     db.db.TestDatabase.insert_one({"name": "John"})
#     return "Connected to the data base!"


# @app.route("/frontend")
# def connect():
#     return {
#         'son': 'Obed'
#     }


@app.route("/processLink", methods=['GET', 'POST'])
def processLink():
    print("hi")
    url = request.json
    combo = find_combosquatting(url)
    print(combo)
    return jsonify(f"Potential Combo Squattings are {combo}")


if __name__ == '__main__':
    app.run()
