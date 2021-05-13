from idn_homographs_database.homograph import homograph
import tldextract
from db import db
from db import upDateDataBase

def count_char_diff(url, squat):
    diff = 0
    for i in range(len(url)):
        if url[i] != squat[i]:
            diff += 1
    return diff


def runTest():
    homoCol = db.get_collection('HomographSquats')
    url = "youtube.com"
    domain, suffix = url.split('.')
    suffix = '.'+suffix
    homograph_generator = homograph.generate_similar_strings(domain)
    # entry = {"_id": str(typoId), "typo": typo, "domain": domain}
    for i in range(10):
        # Let's generate ten homograph squats
        squat = next(homograph_generator) + suffix
        entry = {"_id": str(i), "squat": squat, "domain": url}
        homoCol.replace_one({"_id": str(i)}, entry)
        print(squat)

upDateDataBase()