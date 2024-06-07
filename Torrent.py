import requests
from concurrent.futures import ThreadPoolExecutor as Pool
import json

global jackett_config

try:
    with open("./Config/jackett.json", "r") as f:
        jackett_config = json.load(f)
        print("file opened")
except Exception as e:
    jackett_config = {
        "api_key": "xh0joh233vkuzmjqrhffx7pt2k1y3neb",
        "url": "http://jackett.elchupakabra.lol",
    }
    print("using online api ")


def Search(search, catagory=None):
    t = search
    cat = catagory
    if t == None:
        return "please provide a search term "
    res = []

    def filter(i, catagory=cat):
        if i["catagory"] == catagory:
            return True
        else:
            return False

    def extract_info(i):
        print(f"extracting info :{i}")
        item = {}
        item["Title"] = i["Title"]
        item["catagory"] = i["CategoryDesc"]
        item["source"] = i["Tracker"]
        lnk = i["Link"]
        item["link"] = lnk
        item["magnet"] = i["MagnetUri"]
        item["size"] = i["Size"] / 1024 / 1024 / 1024
        item["size"] = round(item["size"], 2)
        item["size"] = f"{item['size']} GB"
        if item["magnet"] is not None:
            item["qbit"] = True
        else:
            item["qbit"] = False
        if cat == None:
            res.append(item)
        else:
            if filter(item):
                res.append(item)

    url = (
        f"{jackett_config['url']}/api/v2.0/indexers/all/results?apikey={jackett_config['api_key']}&Query="
        + t
    )
    r = requests.get(url)
    print(r)
    r = r.json()
    # r = json.loads(r)
    r = r["Results"]
    print(len(r))
    pool = Pool(1000)
    pool.map(extract_info, (r))
    pool.shutdown(wait=True)
    return res
