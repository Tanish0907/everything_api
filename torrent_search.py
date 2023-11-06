import requests
import pandas
import json
from multiprocessing.dummy import Pool as ThreadPool 
from rich import print
from rich.table import Table
from subprocess import check_output


global res
global jackett_config

with open("./CONFIG/jackett.json") as f:
    jackett_config = json.load(f)
    
res = {}


def filter(i, catagory):
    if i["catagory"] == catagory:
        return True
    else:
        return False    
      
def extract_info(i):
    item = {}
    item["catagory"] = i["CategoryDesc"]
    item["source"] = i['Tracker']
    lnk=i["Link"]
    item["link"] = lnk
    item["magnet"] = i["MagnetUri"]
    item["size"] = i["Size"]/1024/1024/1024
    item["size"] = round(item["size"], 2)
    item["size"] = f"{item['size']} GB"
    if item["magnet"] is not None:
        item["qbit"] = True
    else:
        item["qbit"] = False
    res[i["Title"]]=item
    
def search_torr(catagory,term:str,jackett=jackett_config):
    url = f"{jackett['url']}/api/v2.0/indexers/all/results?apikey={jackett['api_key']}&Query={term}"
    r = requests.get(url)
    r = r.text
    r = json.loads(r)
    r = r["Results"]
    pool = ThreadPool(1000)
    pool.map(extract_info, (r))
    pool.close()
    pool.join()
    if catagory != None:
        for i in list(res.keys()):
            if filter(res[i], catagory) == False:
                del res[i]
    return(res)