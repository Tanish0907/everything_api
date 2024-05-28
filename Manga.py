import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor as Pool
from functools import partial

global manga_res
manga_res = {}
global ch_dict
ch_dict = {}


def get_search(i):
    print(i)
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
    print(manga)


def Mangasearch(keyword: str):
    manga_res.clear()
    if keyword == None:
        return {"Error": "enter a keyword"}

    link = f"https://mangapanda.in/search?q={keyword}"
    r = requests.get(link).text
    soup = bs(r, "lxml")
    manga_results = soup.find_all("a", class_="tooltips")
    pool = Pool(100)
    pool.map(get_search, manga_results)
    pool.shutdown(wait=True)
    return manga_res


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


def Get_manga(manga_name: str, source: str):
    manga_name = manga_name.replace(" ", "-").replace(",", "-").lower()
    if source == "mangapanda":
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
        pool = Pool(100)
        pool.map(get_chapters, ch_list)
        pool.shutdown(wait=True)
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
        pool = Pool(100)
        pool.map(partial(get_rmanga_ch, manganame=manga_name), ch)
        pool.shutdown(wait=True)
        return ch_dict
