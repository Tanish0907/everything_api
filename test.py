# import requests
# from bs4 import BeautifulSoup as bs
# from multiprocessing.dummy import Pool as ThreadPool
# manga_res = {}
# from raincoat import search

"""
        ln = requests.get(i["link"]).text
        soup = bs(ln, 'lxml')
        chapters = soup.find_all('li', class_='row')
        cl_list=[]
        for j in chapters:
            l = j.find('a')
            l = l.get('href')
            ch_list.append(l)
        manga["chapters"]=ch_list
"""


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
# anime_list = {}

# embad_lst = []
# download_lst = []


# def extract_download_link(i):
#     r = requests.get(i).text
#     soup = bs(r, "lxml")
#     download_link = soup.find("li", class_="dowloads")
#     download_link = download_link.find("a").get('href')
#     download_lst.append(download_link)


# def extract_embad_link(link):
#     r = requests.get(link).text
#     soup = bs(r, 'lxml')
#     embad = soup.find("li", class_="filelions")
#     embad = embad.find("a")["data-video"]
#     embad_lst.append(embad)


# def get_anime(name: str = None):
#     anime_list.clear()
#     link = f'https://gogoanimehd.to/search.html?keyword={name}'
#     r = requests.get(link).text
#     soup = bs(r, "lxml")
#     search_res = soup.find('ul', class_="items")
#     links = search_res.find_all("li")
#     for i in links:
#         anime = {}
#         if "Dub" in i.find("a")["title"]:
#             title = i.find("a")['title'].replace("(Dub)", "")
#             anime["DUB_or_SUB"] = "DUB"
#         else:
#             title = i.find("a")['title']
#             anime["DUB_or_SUB"] = "SUB"

#         anime["poster"] = i.find("a").find("img")["src"]
#         anime["release-year"] = i.find("p", class_="released").text.split(
#             ":")[-1].replace(" ", "").replace("\t", "")
#         anime_list[title] = anime

#     print(anime_list)

# f_anime = {}


# def get_anime_info(anime_name: str):
#     anime_name = anime_name.replace(" ", "-")
#     f_anime.clear()
#     link = f"https://gogoanimehd.to/category/{anime_name}"
#     r = requests.get(link).text
#     soup = bs(r, 'lxml')
#     if soup == None:
#         return {"Error": "Anime title not found"}
#     poster = soup.find("div", class_="anime_info_body_bg")
#     poster = poster.find("img")["src"]
#     total_ep = soup.find('ul', {'id': 'episode_page'})
#     total_ep = total_ep.find_all("a")
#     total_ep = total_ep[len(total_ep)-1]["ep_end"]
#     total_ep = int(total_ep)
#     anime_details = soup.find_all("p", class_="type")
#     genre = []
#     for i in anime_details[2].find_all("a"):
#         genre.append(i["title"])
#     f_anime["name"] = anime_name
#     f_anime["genre"] = genre
#     f_anime["poster"] = poster
#     f_anime["episodes"] = total_ep
#     f_anime["watch_online"] = []

#     for i in range(1, total_ep+1):
#         link = f"https://gogoanimehd.to/{anime_name}"
#         x = str(i)
#         f_anime["watch_online"].append(f'{link}-episode-{x}')
#     embad_lst.clear()
#     download_lst.clear()
#     pool = ThreadPool(100)
#     pool.map(extract_embad_link, f_anime["watch_online"])
#     # pool.map(extract_download_link, f_anime["watch_online"])
#     print(pool.close())
#     print(pool.join())
#     print(embad_lst)
#     f_anime["watch_online"] = embad_lst
#     # f_anime["download_link"] = download_lst
#     print(f_anime)

# comic_books={}
# def extract_comic_links(i):
#     comic={}
#     link=i.find("a").get("href")
#     link=f"https://readcomiconline.li{link}"
#     title=i.find("img")["title"].replace(" ","-").replace("(","").replace(")","").lower()
#     poster=i.find("img")["src"]
#     comic["link"]=link
#     comic["poster"]=f"https://readcomiconline.li{poster}"
#     comic_books[title]=comic
# def get_comics(keyword):
#     r=requests.get(f"https://readcomiconline.li/Search/Comic/{keyword}").text
#     soup=bs(r,'lxml')
#     comics=soup.find_all("div",class_="col cover")
#     pool=ThreadPool(5)
#     pool.map(extract_comic_links,comics)
#     pool.close()
#     pool.join()
#     print(comic_books)


# issue_dict={}
# issues_lst=[]
# def get_comic(comicname):
#     print(f'scanning for {comicname}.....')
#     link = f'https://comicextra.net/comic/{comicname}'
#     ln = requests.get(link).text
#     soup = bs(ln, 'lxml')
#     issues = soup.find('table', class_="table")
#     if (issues == None):
#         print(f'comic:{comicname} not found')
#         exit()
#     else:
#         issue_link = issues.find_all('a')


#         for i in issue_link:
#             issues_lst.append(i.get('href')+'/full')
#     print(issues_lst)

# def get_issue(i):
#         links=[]
#         ln = requests.get(i).text
#         soup = bs(ln, "lxml")
#         pages = soup.find('div', class_="chapter-container")
#         page_link = pages.find_all('img')
#         for j in page_link:
#             links.append(j.get('src'))
#         x = i.find('issue')
#         issue_dict[i[x::].replace("/", "-")] = links
# comic_books={}
# def get_comic_details(i):
#     comic={}
#     ancor=i.find("a",class_="image")
#     poster=ancor.find("img")["src"]
#     ancor=ancor.get("href")
#     title=ancor.split("/")[-1]
#     detail=i.find_all("div",class_="detail")
#     status=detail[1].text.split(":")
#     released=detail[2].text.split(":")
#     comic["link"]=ancor
#     comic["poster"]=poster
#     comic[status[0]]=status[-1].replace("\n","")
#     comic[released[0]]=released[-1].replace("\n","")
#     comic_books[title]=comic

# def search(keyword:str=None):
#     link=f"https://comicextra.net/comic-search?key={keyword}"
#     r=requests.get(link).text
#     soup=bs(r,'lxml')
#     soup=soup.find("div",class_="movie-list-index home-v2")
#     comics=soup.find_all("div",class_="cartoon-box")
#     pool=ThreadPool(5)
#     pool.map(get_comic_details,comics)
#     pool.close()
#     pool.join()
#     print(comic_books)

# search("invincible")

# print(search("jujutsu"))
# import requests
# from bs4 import BeautifulSoup as bs
# # manga=requests.get(f'https://rmanga.app/jujutsu-kaisen/chapter-238/all-pages').text
# # soup=bs(manga,'lxml')
# # # chapters=soup.find("div",class_="cm-tabs-conten novels-detail-chapters")
# # chapters=soup.find_all("img")
# # print(chapters)
# ch_dict={}
# def get_rmanga_ch(manga_name,ch_total):
#     for i in range(2,ch_total):
#         manga=requests.get(f'https://rmanga.app/{manga_name}/chapter-{i}/all-pages').text
#         soup=bs(manga,'lxml')
#         pages=soup.find("div",class_="chapter-detail-novel-big-image text-center")
#         pages=pages.find_all("img")
#         pg_lst=[]
#         for j in pages:
#             pg_lst.append(j.get("src"))
#         ch_dict[i]=pg_lst
#     print(ch_dict)
# ch_no=requests.get(f'https://rmanga.app/jujutsu-kaisen/chapter-1/all-pages').text
# soup=bs(ch_no,'lxml')
# ch_total=soup.find_all("option")
# ch=[]
# for i in ch_total:
#     try :
#         eval(i.text.split(" ")[-1])
#         ch.append(i.text.split(" ")[-1])
#     except:
#         pass
# get_rmanga_ch("jujutsu-kaisen",int(ch[0]))
"""from gogoanime import GogoAnime
from requests import Session
s=Session()
a=GogoAnime(session=s)
x=(a.fetchAnimeInfo(anime_id="naruto"))
print(x)"""
# print(a.search(query="jujutsu"))
"""from anime import anime

a = anime("jujutsu kaisen")
# print(a.search())
print(a.get_anime("jujutsu-kaisen-tv"))
"""
from gogoanime import GoGo

Anime = GoGo()
Anime.search("One Piece")
