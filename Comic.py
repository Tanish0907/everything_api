import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor as Pool

global issue_dict
global comic_books
global issues_lst
global comic_book
comic_books = {}
issue_dict = {}
issues_lst = []
comic_book = {}


def get_issue(i):
    links = []
    ln = requests.get(i).text
    soup = bs(ln, "lxml")
    pages = soup.find("div", class_="chapter-container")
    page_link = pages.find_all("img")
    for j in page_link:
        links.append(j.get("src"))
    x = i.find("issue")
    x=eval(i[x::].split("/")[0].split("-")[-1])
    issue_dict[x] = links


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
    comic["id"]=title
    comic["poster"] = poster
    comic[status[0]] = status[-1].replace("\n", "")
    comic[released[0]] = released[-1].replace("\n", "")
    comic_book[title] = comic


def Comicsearch(keyword: str):
    comic_book.clear()
    link = f"https://comicextra.org/search?keyword={keyword}"
    r = requests.get(link).text
    soup = bs(r, "lxml")
    soup = soup.find("div", class_="movie-list-index home-v2")
    comics = soup.find_all("div", class_="cartoon-box")
    print(comics)
    pool = Pool(20)
    pool.map(get_comic_details, comics)
    pool.shutdown(wait=True)
    return comic_book


def Get_comic(comic_name: str):
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

    pool = Pool(100)
    pool.map(get_issue, issues_lst)
    pool.shutdown(wait=True)
    return issue_dict
