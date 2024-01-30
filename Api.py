from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pytube import YouTube, Search
from bs4 import BeautifulSoup as bs
import requests
import pytube.contrib.playlist as pl
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from gogoanime import GogoAnime
from requests import Session
from torrent_search import search_torr

# manag dicts/data
ch_dict = {}
manga_res = {}
# anime dicts/data
anime_list = {}
f_anime = {}
# yt_search data
embad_lst = []
# comic dicts/data
comic_books = {}
issue_dict = {}
issues_lst = []
comic_book = {}
# anime functions


def extract_m3u8_link(dict: dict):
    s = Session()
    a = GogoAnime(s)
    m3u8_links = {}
    id = dict["id"]
    ep = dict["number"]
    m3u8_data = a.fetchEpisodeSources(id)
    for i in m3u8_data["sources"]:
        m3u8_links[i["quality"]] = i["url"]
    s.close()
    return ep, m3u8_links


# manga functions
def get_search(i):
    ln = requests.get(i.get("href")).text
    soup = bs(ln, "lxml")
    chapters = soup.find_all("li", class_="row")
    manga = {}
    title = (
        i["title"]
        .replace("(", "")
        .replace(")", "")
        .replace(" ", "-")
        .replace(":", "")
        .lower()
    )
    manga["link"] = i.get("href")
    manga["cover"] = i.find("img")["src"]
    manga["number of chapters"] = len(chapters)
    manga_res[title] = manga


def get_chapters(link):
    ch = link.split("-")[-1]
    ln = requests.get(link).text
    soup = bs(ln, "lxml")
    page = soup.find("p")
    mang_page_link = list(page.text.split(","))
    ch_dict[ch] = mang_page_link


def get_rmanga_ch(i, manganame):
    manga = requests.get(f"https://rmanga.app/{manganame}/chapter-{i}/all-pages").text
    soup = bs(manga, "lxml")
    pages = soup.find("div", class_="chapter-detail-novel-big-image text-center")
    pages = pages.find_all("img")
    pg_lst = []
    for j in pages:
        pg_lst.append(j.get("src"))
    ch_dict[i] = pg_lst


# comic functions


def get_issue(i):
    links = []
    ln = requests.get(i).text
    soup = bs(ln, "lxml")
    pages = soup.find("div", class_="chapter-container")
    page_link = pages.find_all("img")
    for j in page_link:
        links.append(j.get("src"))
    x = i.find("issue")
    issue_dict[i[x::].replace("/", "-")] = links


def get_comic_details(i):
    comic = {}
    ancor = i.find("a", class_="image")
    poster = ancor.find("img")["src"]
    ancor = ancor.get("href")
    title = ancor.split("/")[-1]
    detail = i.find_all("div", class_="detail")
    status = detail[1].text.split(":")
    released = detail[2].text.split(":")
    comic["link"] = ancor
    comic["poster"] = poster
    comic[status[0]] = status[-1].replace("\n", "")
    comic[released[0]] = released[-1].replace("\n", "")
    comic_book[title] = comic


app = FastAPI()


@app.get("/")
def home():
    return {"Success": "api is up and running,gg"}


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
            video_stat["length"] = format(vid.length / 60, ".2f")
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
    s = Session()
    gogo = GogoAnime(s)
    anime_list = gogo.search(query=keyword)
    s.close()
    return anime_list


@app.get("/anime/{anime_name}")
def get_anime_info(anime_name: str, episode_id: Optional[int] = None):
    f_anime.clear()
    s = Session()
    gogo = GogoAnime(s)
    anime = gogo.fetchAnimeInfo(anime_id=anime_name)
    f_anime["name"] = anime["id"]
    f_anime["genre"] = anime["genres"]
    f_anime["poster"] = anime["image"]
    f_anime["total episodes"] = anime["totalEpisodes"]
    # if episode_id == None:
    #     f_anime["episodes"]=anime["episodes"]
    if episode_id != None:
        f_anime["m3u8"] = {}
        for i in anime["episodes"]:
            if i["number"] == episode_id:
                i = extract_m3u8_link(i)
                f_anime["m3u8"][i[0]] = i[1]
                break
        # pool=ThreadPool(100)
        # links=pool.map(extract_m3u8_link,anime["episodes"])
        # for i in links:
        #     f_anime["m3u8"][i[0]]=i[1]
    return f_anime


@app.get("/books/manga")
def manga():
    return {"manga": "working"}


@app.get("/books/manga/search")
def search(keyword: str = None):
    manga_res.clear()
    if keyword == None:
        return {"Error": "enter a keyword"}

    link = f"https://mangapanda.in/search?q={keyword}"
    r = requests.get(link).text
    soup = bs(r, "lxml")
    manga_results = soup.find_all("a", class_="tooltips")
    pool = ThreadPool(100)
    pool.map(get_search, manga_results)
    print(pool.close())
    print(pool.join())

    return manga_res


@app.get("/books/manga/{manga_name}")
def get_manga(manga_name: str, source: Optional[str] = None):
    manga_name = manga_name.replace(" ", "-").lower()
    if source == "mangapanda" or source == None:
        # idk=get_chapters_readmanga_online(search_manga(manga_name))
        # return idk
        ch_dict.clear()
        manga = requests.get(f"https://mangapanda.in/manga/{manga_name}").text
        soup = bs(manga, "lxml")
        chapters = soup.find_all("li", class_="row")
        ch_list = []
        for i in chapters:
            l = i.find("a")
            l = l.get("href")
            ch_list.append(l)
        pool = ThreadPool(100)
        pool.map(get_chapters, ch_list)
        print(pool.close())
        print(pool.join())
        return ch_dict
    elif source == "rmanga":
        ch_dict.clear()
        ch_no = requests.get(
            f"https://rmanga.app/{manga_name}/chapter-1/all-pages"
        ).text
        soup = bs(ch_no, "lxml")
        ch_total = soup.find_all("option")
        ch_total = soup.find_all("option")
        ch = []
        for i in ch_total:
            try:
                eval(i.text.split(" ")[-1])
                ch.append(int(i.text.split(" ")[-1]))
            except:
                pass
        pool = ThreadPool(100)
        pool.map(partial(get_rmanga_ch, manganame=manga_name), ch)
        print(pool.close())
        print(pool.join())
        return ch_dict


@app.get("/books/comics")
def comics():
    return {"comics": "working"}


@app.get("/books/comics/search")
def search(keyword: str = None):
    comic_books.clear()
    link = f"https://comicextra.net/comic-search?key={keyword}"
    r = requests.get(link).text
    soup = bs(r, "lxml")
    soup = soup.find("div", class_="movie-list-index home-v2")
    comics = soup.find_all("div", class_="cartoon-box")
    pool = ThreadPool(20)
    pool.map(get_comic_details, comics)
    print(pool.close())
    print(pool.join())
    return comic_book


@app.get("/books/comics/{comic_name}")
def get_comic(comic_name: str = None):
    issues_lst.clear()
    issue_dict.clear()
    link = f"https://comicextra.net/comic/{comic_name}"
    ln = requests.get(link).text
    soup = bs(ln, "lxml")
    issues = soup.find("table", class_="table")
    if issues == None:
        print(f"comic:{comic_name} not found")
        exit()
    else:
        issue_link = issues.find_all("a")
        for i in issue_link:
            issues_lst.append(i.get("href") + "/full")

    pool = ThreadPool(100)
    pool.map(get_issue, issues_lst)
    pool.close()
    pool.join()
    return issue_dict


@app.get("/torrents/search/")
def torr_search(search_term: str = None, catagory: Optional[str] = None):
    if search_term == None:
        return {"Error": "enter a search term"}
    search_term = search_term.replace(" ", "+")
    results = search_torr(catagory, search_term)
    return results
