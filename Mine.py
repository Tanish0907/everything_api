import requests
import pandas as pd
import pickle
import os
from supabase import create_client, Client
from PIL import Image
import numpy as np
import json
from io import BytesIO
url: str="https://ncnbbvpfaknujvlhwzzk.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5jbmJidnBmYWtudWp2bGh3enprIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYzODU0MTgsImV4cCI6MjAzMTk2MTQxOH0.KjjA-DeS00Ta4G9d3d9fEnvdGi78aHrQV3Ns7t52E18"
conn: Client = create_client(url, key)
# from concurrent.futures import ProcessPoolExecutor as Ppool
# from concurrent.futures import as_completed as Complete
# from multiprocessing.dummy import Pool as Tpool
# from concurrent.futures import wait as Wait, ALL_COMPLETED as All


def continue_db(manga_list: list):
    with open("logs.txt", "r") as f:
        lst = f.readlines()
        if not lst:
            return manga_list
        else:
            for i in lst:
                if i=="\n":
                    return manga_list
                else:
                    manga_list.pop(manga_list.index(i.lstrip().replace("\n", "").rstrip()))
    return manga_list


def save_manga_obj(obj_list: list):
    for i in obj_list:
        if f"{i.manga_name}.obj" in os.listdir("./.obj/"):
            pass
        else:
            with open(f"./.obj/{i.manga_name}.obj", "wb") as f:
                pickle.dump(i, f)
                print(f"{i.manga_name}:saved")
    print("all_obj saved")


def create_manga_list(path):
    manga_name_list = pd.read_csv(path)["title"]
    manga_list = [
        i.lower()
        .replace("-", "")
        .replace(",", "")
        .replace("novel", "")
        .replace("special", "")
        .replace("part", "")
        .replace("webcomic", "")
        .replace("1", "")
        .replace("2", "")
        .replace("3", "")
        .replace("7", "")
        .replace("(", "")
        .replace(")", "")
        .replace(":", "")
        .replace("!", "")
        .rstrip()
        .lstrip()
        .replace(" ", "-")
        for i in manga_name_list
    ]
    manga_list = continue_db(manga_list)
    return list(set(manga_list))


class Manga:
    def __init__(self, manga_name: str, api_url="http://localhost:8000/manga"):
        self.manga_name = manga_name
        print(f"creating_obj:{manga_name}")
        try:
            self.book = requests.get(f"{api_url}/{manga_name}").json()
            self.book_ch = [eval(i) for i in list(self.book.keys())]
            self.book_ch.sort()
            self.pages=[]
            for i in self.book_ch:
                for pg in self.book[str(i)]:
                    self.pages.append(pg)
        except Exception as e:
            self.book = {}
        if bool(self.book):
            self.empty = False
        else:
            self.empty = True
        self.created = False
        print(f"obj_made:{manga_name}")

    def add_to_db(self):
        if self.empty:
            return f"no entry found!:{self.manga_name}"
        else:
            manga_name = self.manga_name.replace("-", "_")
            try:
                for i in self.pages:
                    # img_bin=requests.get(i).content
                    # img_bin=json.dumps({"bin":f"{img_bin}"})
                    data,count=conn.table('manga').insert({"manga":f"{self.manga_name}","image_url":i,"img_bin":None}).execute()
                    print(f"data:{data}\ncount:{count}")
                print(f"entries made:{len(self.pages)}!!")
                self.created=True
                os.remove(f"./.obj/{self.manga_name}.obj")
                print(f"done:{self.manga_name} to db")
                with open("logs.txt", "a") as file:
                    file.write(f"\n{self.manga_name.replace('_','-')}")
                return f"added{self.manga_name}"
            except Exception as e:
                print(f"couldn't add the {self.manga_name} to firebase :{e}")
                return f"{self.manga_name}:not added!!"

class Mine:
    def __init__(self, mine_name: list):
        if not os.listdir("./.obj/"):
            manga_obj_list = [self.init_obj_list(i) for i in mine_name]
            self.manga_obj = []
            for i in manga_obj_list:
                if i is None:
                    continue
                else:
                    self.manga_obj.append(i)
            print("saving_manga_obj...")
            save_manga_obj(self.manga_obj)
            print(
                "*******************************************************obj saved********************************************************"
            )
        else:
            manga_obj_list = []
            self.manga_obj = []
            log = open("./logs.txt", "r")
            logs = log.readlines()
            for i in os.listdir("./.obj/"):
                file = open(f"./.obj/{i}", "rb")
                obj = pickle.load(file)
                if obj.manga_name.replace("_", "-") in logs:
                    pass
                else:
                    self.manga_obj.append(obj)
            print(self.manga_obj)
            print(
                "***************************************************obj appended********************************************************"
            )

    def init_obj_list(self, name):
        obj = Manga(name)
        if obj.empty:
            print(f"not appended:{obj.manga_name}")
            return None
        else:
            print(f"added:{obj.manga_name}:{len(obj.book)}\n{obj.book_ch}")
            return obj

    def start_mine(self):
        for i in self.manga_obj:
            print(i.add_to_db())


manga_list = create_manga_list("./data.csv")
mine = Mine(manga_list)
mine.start_mine()
