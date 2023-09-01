from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pytube import YouTube
import pytube.contrib.playlist as pl

app = FastAPI()


@app.get("/")
def home():
    return {"Success": "api is up and running"}


@app.get("/info/id")
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
