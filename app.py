from flask import Flask

app = Flask(__name__)


@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"


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


if __name__ == '__main__':
    app.run()
