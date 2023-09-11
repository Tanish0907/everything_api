from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pytube import YouTube, Search
from bs4 import BeautifulSoup as bs
import requests
import pytube.contrib.playlist as pl
from multiprocessing.dummy import Pool as ThreadPool

ch_dict = {}
anime_list = {}
manga_res = {}
embad_lst = []
download_lst = []
f_anime = {}
comic_books={}

def extract_comic_links(i):
    comic={}
    link=i.find("a").get("href")
    link=f"https://readcomiconline.li{link}"
    title=i.find("img")["title"].replace(" ","-").replace("(","").replace(")","").lower()
    poster=i.find("img")["src"]
    comic["link"]=link
    comic["poster"]=f"https://readcomiconline.li{poster}"
    comic_books[title]=comic

def extract_download_link(i):
    r = requests.get(i).text
    soup = bs(r, "lxml")
    download_link = soup.find("li", class_="dowloads")
    download_link = download_link.find("a").get('href')
    download_lst.append(download_link)


def extract_embad_link(link):
    r = requests.get(link).text
    soup = bs(r, 'lxml')
    embad = soup.find("li", class_="filelions")
    embad = embad.find("a")["data-video"]
    embad_lst.append(embad)


def get_search(i):
    ln = requests.get(i.get("href")).text
    soup = bs(ln, 'lxml')
    chapters = soup.find_all('li', class_='row')
    manga = {}
    manga["link"] = i.get("href")
    manga["cover"] = i.find("img")["src"]
    manga["number of chapters"] = len(chapters)
    manga_res[i["title"]] = manga


def get_chapters(link):
    ch = link.split("-")[-1]
    ln = requests.get(link).text
    soup = bs(ln, 'lxml')
    page = soup.find('p')
    mang_page_link = list(page.text.split(","))
    ch_dict[ch] = mang_page_link


app = FastAPI()


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
def get_anime(keyword: str = None):
    anime_list.clear()
    link = f'https://gogoanimehd.to/search.html?keyword={keyword}'
    r = requests.get(link).text
    soup = bs(r, "lxml")
    search_res = soup.find('ul', class_="items")
    links = search_res.find_all("li")
    for i in links:
        anime = {}
        if "Dub" in i.find("a")["title"]:
            title = i.find("a")['title'].replace("(Dub)", "")
            link = i.find("a").get("href")
            anime["DUB_or_SUB"] = "DUB"
        else:
            link = i.find("a").get("href")
            title = i.find("a")['title']
            anime["DUB_or_SUB"] = "SUB"
        anime["name"] = i.find("a")["title"].replace(
            "(", "").replace(")", "").replace(" ", "-").lower()
        anime["link"] = f'https://gogoanimehd.to{link}'
        anime["poster"] = i.find("a").find("img")["src"]
        anime["release-year"] = i.find("p", class_="released").text.split(
            ":")[-1].replace(" ", "").replace("\t", "")
        anime_list[title] = anime

    return (anime_list)


@app.get("/anime/{anime_name}")
def get_anime_info(anime_name: str):
    anime_name = anime_name.replace(" ", "-")
    f_anime.clear()
    link = f"https://gogoanimehd.to/category/{anime_name}"
    r = requests.get(link).text
    soup = bs(r, 'lxml')
    if soup == None:
        return {"Error": "Anime title not found"}
    poster = soup.find("div", class_="anime_info_body_bg")
    poster = poster.find("img")["src"]
    total_ep = soup.find('ul', {'id': 'episode_page'})
    total_ep = total_ep.find_all("a")
    total_ep = total_ep[len(total_ep)-1]["ep_end"]
    total_ep = int(total_ep)
    anime_details = soup.find_all("p", class_="type")
    genre = []
    for i in anime_details[2].find_all("a"):
        genre.append(i["title"])
    if "dub" in anime_name:
        f_anime["SUB_or_DUB"] = "DUB"
    else:
        f_anime["SUB_or_DUB"] = "SUB"
    f_anime["name"] = anime_name
    f_anime["genre"] = genre
    f_anime["poster"] = poster
    f_anime["episodes"] = total_ep
    f_anime["watch_online"] = []

    for i in range(1, total_ep+1):
        link = f"https://gogoanimehd.to/{anime_name}"
        x = str(i)
        f_anime["watch_online"].append(f'{link}-episode-{x}')
    embad_lst.clear()
    download_lst.clear()
    pool = ThreadPool(100)
    pool.map(extract_embad_link, f_anime["watch_online"])
    # pool.map(extract_download_link, f_anime["watch_online"])
    print(pool.close())
    print(pool.join())
    f_anime["watch_online"] = embad_lst
    # f_anime["download_link"] = download_lst
    return (f_anime)


@app.get("/books/manga")
def manga():
    return {"manga": "working"}


@app.get("/books/manga/search")
def search(keyword: str = None):
    manga_res.clear()
    if keyword == None:
        return {"Error": "enter a keyword"}
    link = f'https://mangapanda.in/search?q={keyword}'
    r = requests.get(link).text
    soup = bs(r, "lxml")
    manga_results = soup.find_all("a", class_="tooltips")
    # for i in manga_results:
    #     ln = requests.get(i.get("href")).text
    #     soup = bs(ln, 'lxml')
    #     chapters = soup.find_all('li', class_='row')
    #     manga = {}
    #     manga["cover"] = i.find("img")["src"]
    #     manga["number of chapters"] = len(chapters)
    #     manga_res[i["title"]] = manga
    pool = ThreadPool(5)
    pool.map(get_search, manga_results)
    print(pool.close())
    print(pool.join())
    return (manga_res)


@app.get("/books/manga/{manga_name}")
def get_manga(manga_name: str):
    manga_name = manga_name.replace(" ", "-").lower()
    manga = requests.get(f'https://mangapanda.in/manga/{manga_name}').text
    soup = bs(manga, 'lxml')
    chapters = soup.find_all('li', class_='row')
    ch_list = []
    for i in chapters:
        l = i.find('a')
        l = l.get('href')
        ch_list.append(l)
    pool = ThreadPool(50)
    pool.map(get_chapters, ch_list)
    print(pool.close())
    print(pool.join())
    return ch_dict


@app.get("/books/comics")
def comics():
    return ({"comics": "working"})

@app.get("/books/comics/search")
def get_comics(keyword):
    comic_books.clear()
    r=requests.get(f"https://readcomiconline.li/Search/Comic/{keyword}").text
    soup=bs(r,'lxml')
    comics=soup.find_all("div",class_="col cover")
    pool=ThreadPool(5)
    pool.map(extract_comic_links,comics)
    print(pool.close())
    print(pool.join())
    return comic_books
    