from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pytube import YouTube
from bs4 import BeautifulSoup as bs
import requests
import pytube.contrib.playlist as pl

app = FastAPI()


class anime(BaseModel):
    name: str
    genre: str
    episodes: int


anime_list = {}
'''
class anime:
    def __init__(self, anime_name):
        self.animename = anime_name.replace(" ", "%20")
        self.anime_list = {}
        self.ep_list = []
        self.download_links = []

    def get_anime(self):
        link = f'https://gogoanimehd.to/search.html?keyword={self.animename}'
        r = requests.get(link).text
        soup = bs(r, "lxml")
        search_res = soup.find('ul', class_="items")
        links = search_res.find_all("a")
        for i in links:
            if ('Dub' in i['title']):
                self.anime_list[i['title']
                                ] = f"https://gogoanimehd.to{i.get('href')}"
        n = 0
        for i in list(self.anime_list.keys()):
            print(f'{n}:{i}:{self.anime_list[i]}')
            n += 1

    def get_episodes(self, n):
        print('===================================watch-online=======================================')
        selected_anime = list(self.anime_list.keys())[n]
        link = self.anime_list[selected_anime]
        r = requests.get(link).text
        soup = bs(r, 'lxml')
        total_ep = soup.find('ul', {'id': 'episode_page'})
        total_ep = total_ep.find("a")['ep_end']
        total_ep = int(total_ep)
        link = link.replace("category/", "")
        for i in range(1, total_ep+1):
            x = str(i)
            print(f'{link}-episode-{x}')
            self.ep_list.append(f'{link}-episode-{x}')
        return self.ep_list

    def get_download_link(self):
        print('===================================download-links========================================')
        for i in self.ep_list:
            r = requests.get(i).text
            soup = bs(r, "lxml")
            download_link = soup.find("li", class_="dowloads")
            download_link = download_link.find("a").get('href')
            print(download_link)
            self.download_links.append(download_link)
        return self.download_links
def watch_anime(name):
    a = anime(name)
    a.get_anime()
    x = eval(input("enter anime no.:"))
    ep_list = a.get_episodes(x)
    download_list = a.get_download_link()
    return (ep_list, download_list)

'''


@app.get("/")
def home():
    return {"Success": "api is up and running"}


@app.get("/youtube/info/id")
def get_info(id: Optional[str] = None):
    if id == None:
        return {"Error": "enter vid id"}
    try:
        link = f"https://www.youtube.com/watch?v={id}"
        vid = YouTube(link)
        video_stat = {}
        video_stat["type"] = "video"
        video_stat["title"] = vid.title
        video_stat["views"] = vid.views
        video_stat["length"] = format(vid.length/60, ".2f")
        video_stat["video_thumbnail"] = vid.thumbnail_url
        video_stat["file_link"] = vid.embed_url
        return video_stat
    except:
        try:
            link = f"https://www.youtube.com/playlist?list={id}"
            plist = pl.Playlist(link)
            playlist_stat = {}
            playlist_stat["type"] = "playlist"
            playlist_stat["title"] = plist.title
            playlist_stat["views"] = plist.views
            playlist_stat["number of videos"] = plist.length
            playlist_stat["videos"] = plist.videos
            return playlist_stat
        except:
            return {"Error": "NOT A VALID ID"}


@app.get("/anime")
def anime():
    return {"anime": "working"}


@app.get("/anime/anime_name")
def get_anime(animename: Optional[str] = None):
    link = f'https://gogoanimehd.to/search.html?keyword={animename}'
    r = requests.get(link).text
    soup = bs(r, "lxml")
    search_res = soup.find('ul', class_="items")
    links = search_res.find_all("a")
    for i in links:
        if ('Dub' in i['title']):
            anime_list[i['title']
                       ] = f"https://gogoanimehd.to{i.get('href')}"
    return (anime_list)
