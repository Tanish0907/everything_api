from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pytube import YouTube, Search
from bs4 import BeautifulSoup as bs
import requests
import pytube.contrib.playlist as pl

app = FastAPI()

anime_list = {}


@app.get("/")
def home():
    return {"Success": "api is up and running"}


@app.get("/youtube/search")
def get_info(*, id: Optional[str] = None, name: Optional[str] = None):
    if id == None and name == None:
        return {"Error": "enter vid id or a name"}
    if name == None:
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
    elif id == None:

        yt_search = {}

        s = Search(name)
        res = 0
        for i in s.results:
            vid = {}
            vid["video_id"] = i.video_id
            vid["embed_link"] = i.embed_url
            vid["creator"] = i._author
            vid["title"] = i.title
            vid["thumbnail"] = YouTube(i.watch_url).thumbnail_url
            yt_search[res] = vid
            res += 1
        return yt_search


@app.get("/anime")
def anime():
    return {"anime": "working"}


@app.get("/anime/search")
def get_anime(name: Optional[str] = None):
    anime_list.clear()
    link = f'https://gogoanimehd.to/search.html?keyword={name}'
    r = requests.get(link).text
    soup = bs(r, "lxml")
    search_res = soup.find('ul', class_="items")
    links = search_res.find_all("a")
    for i in links:
        if ('Dub' in i['title']):
            anime_list[i['title']
                       ] = f"https://gogoanimehd.to{i.get('href')}"
    return (anime_list)


@app.get("/anime/{anime_name}")
def get_anime_info(anime_name: str):
    anime_name = anime_name.replace(" ", "-")
    anime = {}
    link = f"https://gogoanimehd.to/category/{anime_name}"
    r = requests.get(link).text
    soup = bs(r, 'lxml')
    if soup == None:
        return {"Error": "Anime title not found"}
    poster = soup.find("div", class_="anime_info_body_bg")
    poster = poster.find("img")["src"]
    total_ep = soup.find('ul', {'id': 'episode_page'})
    total_ep = total_ep.find("a")['ep_end']
    total_ep = int(total_ep)
    anime_details = soup.find_all("p", class_="type")
    genre = []
    for i in anime_details[2].find_all("a"):
        genre.append(i["title"])
    anime["name"] = anime_name
    anime["genre"] = genre
    anime["poster"] = poster
    anime["episodes"] = total_ep
    anime["watch_online"] = []
    anime["download_links"] = []
    for i in range(1, total_ep+1):
        link = f"https://gogoanimehd.to/{anime_name}"
        x = str(i)
        anime["watch_online"].append(f'{link}-episode-{x}')
    for i in anime["watch_online"]:
        r = requests.get(i).text
        soup = bs(r, "lxml")
        download_link = soup.find("li", class_="dowloads")
        download_link = download_link.find("a").get('href')
        anime["download_links"].append(download_link)
    return anime
