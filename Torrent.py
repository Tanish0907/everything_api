import requests
import json
from multiprocessing.dummy import Pool as ThreadPool

global jackett_config
jackett_config = {
    "api_key": "jr8hzydappm8okpnr9dp2dzn0bmdeyje",
    "url": "https://jackett-ttda.onrender.com",
}


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
    r = r.text
    r = json.loads(r)
    r = r["Results"]
    print(len(r))
    pool = ThreadPool(1000)
    pool.map(extract_info, (r))
    pool.close()
    pool.join()
    return res
