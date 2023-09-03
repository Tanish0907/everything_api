import requests
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool as ThreadPool
# manga_res = {}

'''
        ln = requests.get(i["link"]).text
        soup = bs(ln, 'lxml')
        chapters = soup.find_all('li', class_='row')
        cl_list=[]
        for j in chapters:
            l = j.find('a')
            l = l.get('href')
            ch_list.append(l)
        manga["chapters"]=ch_list
'''


# def get_chapters(link):
#     pg_req = requests.get(link).text
#     soup = bs(pg_req, "lxml")
#     soup = soup.find("div", class_="comic_wraCon text-center")
#     print(soup)
#     page = soup.find_all("img")
#     for i in page:
#         print(i)
# ch_dict = {}


# def get_chapters(ch_list):
#     for i in ch_list:
#         ch = i.split("-")[-1]
#         ln = requests.get(i).text
#         soup = bs(ln, 'lxml')
#         page = soup.find('p')
#         mang_page_link = list(page.text.split(","))
#         ch_dict[ch] = mang_page_link
#         ch = ch+1
#     print(ch_dict)


# def get_manga(manga_name: str):
#     manga_name = manga_name.replace(" ", "-")
#     ch_dict = []
#     manga = requests.get(f'https://mangapanda.in/manga/{manga_name}').text
#     soup = bs(manga, 'lxml')
#     chapters = soup.find_all('li', class_='row')
#     for i in chapters:
#         l = i.find('a')
#         l = l.get('href')
#         ch_dict.append(l)
#     return ch_dict


# def search(keyword: str = None):
#     if keyword == None:
#         return {"Error": "enter a keyword"}
#     link = f'https://mangapanda.in/search?q={keyword}'
#     r = requests.get(link).text
#     soup = bs(r, "lxml")
#     manga_results = soup.find_all("a", class_="tooltips")
#     manga_ind = 0
#     for i in manga_results:
#         manga = {}
#         manga["title"] = i["title"]
#         manga["cover"] = i.find("img")["src"]
#         ln = requests.get(i.get("href")).text
#         soup = bs(ln, 'lxml')
#         chapters = soup.find_all('li', class_='row')
#         ch_list = []
#         for j in chapters:
#             l = j.find('a')
#             l = l.get('href')
#             ch_list.append(l)
#         manga["chapters"] = ch_list

#         manga_res[manga_ind] = manga
#         manga_ind += 1
#     print(manga_res)


# search("jujutsu")
# get_chapters("https://mangapanda.in/baki-dou-2018-chapter-3")
# ch = get_manga("baki-dou-2018")
# get_chapters(ch)
# pool = ThreadPool(10)
# ch_dict = {}


# def get_chapters(link):
#     ch = link.split("-")[-1]
#     ln = requests.get(link).text
#     soup = bs(ln, 'lxml')
#     page = soup.find('p')
#     mang_page_link = list(page.text.split(","))
#     ch_dict[ch] = mang_page_link


# def get_manga(manga_name: str):
#     manga_name = manga_name.replace(" ", "-")
#     ch_list = []
#     manga = requests.get(f'https://mangapanda.in/manga/{manga_name}').text
#     soup = bs(manga, 'lxml')
#     chapters = soup.find_all('li', class_='row')
#     for i in chapters:
#         l = i.find('a')
#         l = l.get('href')
#         ch_list.append(l)
#     return ch_list


# res = pool.map(get_chapters, get_manga("baki-dou-2018"))
# print(pool.close())
# print(pool.join())

# print(ch_dict)
anime_list = {}


def get_anime(name: str = None):
    anime_list.clear()
    link = f'https://gogoanimehd.to/search.html?keyword={name}'
    r = requests.get(link).text
    soup = bs(r, "lxml")
    search_res = soup.find('ul', class_="items")
    links = search_res.find_all("li")
    for i in links:
        anime = {}
        l = i.find("a").get("href")
        anime["link"] = f"https://gogoanimehd.to{l}"
        anime["poster"] = i.find("a").find("img")["src"]
        anime["release-year"] = i.find("p", class_="released").text.split(
            ":")[-1].replace(" ", "").replace("\t", "")
        anime_list[i.find("a")['title']
                   ] = anime

    return (anime_list)


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
    total_ep = total_ep.find_all("a")
    total_ep = total_ep[len(total_ep)-1]["ep_end"]
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
    print(anime)


get_anime("naruto")
