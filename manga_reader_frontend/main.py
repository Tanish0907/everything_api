from os import wait
import customtkinter as c
from tkinter import *
import threading as t
from concurrent.futures import ThreadPoolExecutor as Pool
import asyncio
from PIL import Image
from io import BytesIO
from customtkinter.windows.widgets import image
import requests
from db_req import fetch
from load_manga import Manga
class Main(c.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("430x910")
        self.resizable(0, 0)
        self.term=c.StringVar()
        self.progress_bar=c.CTkProgressBar(self,width=430,corner_radius=30,border_width=2)
        self.progress_bar.pack(padx=0,pady=0)
        self.progress_bar.set(0)
        entry=c.CTkEntry(self,placeholder_text="search_term",textvariable=self.term)
        entry.pack(padx=10,pady=10)
        btn=c.CTkButton(self,text="search",command=self.search_thread)
        btn.pack(padx=10,pady=10)
        self.thread_status=c.CTkLabel(self,text="")
        self.thread_status.pack(padx=10,pady=10)
        self.frame=c.CTkFrame(self,height=900,width=420,corner_radius=10,fg_color="#4e4c4a")
        self.frame.pack(padx=10,pady=10)
        self.frame.pack_propagate(False)
        self.empty=c.CTkLabel(self.frame,text="")
        self.empty.pack(padx=10,pady=10)

    def search_term(self):
        results=fetch(self.term.get())
        return results
    async def get_all(self):
        manga_obj_list={}
        self.info_list=list(self.res.items())
        self.length=len(self.info_list)
        def create_obj(i):
            name=i[0]
            info=i[-1]
            manga_obj_list[name]=Manga(name,info)
            percentage=(self.info_list.index(i)+1)/self.length
            self.progress_bar.set(value=percentage)
            print(f"created:{name}:{percentage}")
            
        pool=Pool(10)
        pool.map(create_obj,self.info_list)
        pool.shutdown(wait=True)
        return manga_obj_list
    def search(self):
        self.res=self.search_term()
        self.key_list=list(self.res.keys())
        if not self.key_list:
            self.empty.configure(text="manga not found")
            self.empty.update()
        else:
            self.empty.configure(text="")
            self.empty.update()
            self.options=c.CTkOptionMenu(self.frame,corner_radius=10,values=self.key_list,dynamic_resizing=True,button_hover_color="#ffffff",command=self.update_)
            self.options.pack(padx=10,pady=10)
            poster=requests.get(self.res[self.key_list[0]]["cover"]).content
            poster=Image.open(BytesIO(poster))
            image=c.CTkImage(poster,size=(280,415))
            self.poster=c.CTkLabel(self.frame,text="",image=image,corner_radius=10)
            self.poster.pack(padx=10,pady=10)
            self.title_book=c.CTkLabel(self.frame,text=self.key_list[0])
            self.title_book.pack(padx=10,pady=10)
            self.manga_obj_list=asyncio.run(self.get_all())
            self.read_btn=c.CTkButton(self.frame,corner_radius=10,text="Read Book",command=lambda: Manga_reader(self.manga_obj_list[self.key_list[0]]))
            self.read_btn.pack(padx=10,pady=10)



        #print(self.res)
    def update_(self,name):
        image=requests.get(self.res[name]["cover"]).content
        image=Image.open(BytesIO(image))
        image=c.CTkImage(image,size=(280,415))
        self.poster.configure(image=image)
        self.poster.update()
        self.title_book.configure(text=name)
        self.title_book.update()
        self.read_btn.configure(command=lambda: Manga_reader(self.manga_obj_list[name]))
        self.read_btn.update()
    def search_thread(self):
        search_thrd = t.Thread(target=self.search)
        search_thrd.start()
        self.check_thread(search_thrd)
    def check_thread(self, thread):
        """Check if the thread is still running."""
        if thread.is_alive():
            self.thread_status.configure(text="running")
            app.after(200, self.check_thread, thread)
        else:
            self.thread_status.configure(text="Thread has finished")

class Manga_reader(c.CTkToplevel):
    def __init__(self,obj:Manga):
        super().__init__()
        self.obj=obj
        self.book=obj.book
        print(self.book.keys())
        self.title("idk")
        self.ch=1
        self.page_no=0
        self.total_pages_ch=len(self.book[str(self.ch)])
        self.display_page()
        self.next_btn = c.CTkButton(
            self, text=">", command=self.next, width=30, height=30
        )
        self.next_btn.place(relx=0.99, rely=0.5, anchor=c.CENTER)
        self.previous_btn = c.CTkButton(
            self, text="<", command=self.previous, width=30, height=30
        )
        self.previous_btn.place(relx=0.01, rely=0.5, anchor=c.CENTER)
    def display_page(self):
        img = requests.get(self.book[str(self.ch)][self.page_no]).content
        img = Image.open(BytesIO(img))
        img = c.CTkImage(img, size=(800, 1000))
        self.page = c.CTkLabel(self, text="", image=img)
        self.page.place(relx=0.5, rely=0.5, anchor=c.CENTER)

    def next(self):
        self.page_no+=1
        try:
            img=requests.get(self.book[str(self.ch)][self.page_no]).content
            img=Image.open(BytesIO(img))
            img=c.CTkImage(img,size=(800,1000))
            self.page.configure(image=img)
            self.page.update()
        except IndexError as e:
            self.ch+=1
            self.page_no=0
            img=requests.get(self.book[str(self.ch)][self.page_no]).content
            img=Image.open(BytesIO(img))
            img=c.CTkImage(img,size=(800,1000))
            self.page.configure(image=img)
            self.page.update()
    def previous(self):
        self.page_no=self.page_no-1
        try:
            img=requests.get(self.book[str(self.ch)][self.page_no]).content
            img=Image.open(BytesIO(img))
            img=c.CTkImage(img,size=(800,1000))
            self.page.configure(image=img)
            self.page.update()
        except IndexError as e:
            self.ch=self.ch-1
            if self.ch<0:
                self.ch=0
            self.page_no=self.page_no-1
            if self.page_no<0:
                self.page_no=0
            img=requests.get(self.book[str(self.ch)][self.page_no]).content
            img=Image.open(BytesIO(img))
            img=c.CTkImage(img,size=(800,1000))
            self.page.configure(image=img)
            self.page.update()


        
if __name__=="__main__":
    app=Main()
    app.mainloop()
