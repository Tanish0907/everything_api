import requests
from PIL import Image
from io import BytesIO
from db_req import fetch_book
from tkinter import *
from concurrent.futures import ThreadPoolExecutor as Pool
class Manga:
    def __init__(self,name:str,res_item:dict):
        self.name=name
        #self.poster=requests.get(res_item["cover"]).content
        #self.poster=Image.open(BytesIO(self.poster))
        self.chapters=res_item["number of chapters"]
        self.book=fetch_book(name)
        '''
        self.pages=self.create_pages()
    def create_pages(self):
        print(f"creating-pages:{self.name}")
        book=[]
        for i in list(self.book.keys()):
            print(f"{i}")
            book.extend(self.convert_to_ctk(self.book[i]))
        return book
    def convert_to_ctk(self,lst:list)->list:
        img_list=[]
        for i in lst:
            print(i)
            img=requests.get(i).content
            img=Image.open(BytesIO(i))
            img_list.append(img)
            print("done")
        return img_list
        '''
