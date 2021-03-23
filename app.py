from flask import Flask, request, jsonify
from flask_cors import CORS
from generateTypo import ts_models
import tldextract

app = Flask(__name__)
cors = CORS(app)

from db import results


@app.route("/processLink", methods=['GET', 'POST'])
def processLink():
    typo = ts_models()
    links = request.json
    firstLink = links[0].lower()
    parts = tldextract.extract(firstLink)
    cl_domain = [parts.domain, '.' + parts.suffix]
    f_clean_domain = ''.join(cl_domain)
    print(f"first link is {f_clean_domain}")
    for doc in results:
        print(f"Here is doc {doc['Domain']}")
        potTypos = typo.generate_ts_domains(doc['Domain'])
        print(f"PotTypos: {potTypos}")
        for sub in potTypos:
            print(potTypos[sub])
            if f_clean_domain in potTypos[sub]:
                return jsonify(f"ALERT!!! Suspicious link ({firstLink}) detected!")
    return jsonify("The coast is clear!")


if __name__ == '__main__':
    app.run()
