import requests
from bs4 import BeautifulSoup as bs
manga_res = {}

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
ch_dict = {}


def get_chapters(ch_list):
    for i in ch_list:
        ch = i.split("-")[-1]
        ln = requests.get(i).text
        soup = bs(ln, 'lxml')
        page = soup.find('p')
        mang_page_link = list(page.text.split(","))
        ch_dict[ch] = mang_page_link
        ch = ch+1
    print(ch_dict)


def get_manga(manga_name: str):
    manga_name = manga_name.replace(" ", "-")
    ch_dict = []
    manga = requests.get(f'https://mangapanda.in/manga/{manga_name}').text
    soup = bs(manga, 'lxml')
    chapters = soup.find_all('li', class_='row')
    for i in chapters:
        l = i.find('a')
        l = l.get('href')
        ch_dict.append(l)
    return ch_dict


def search(keyword: str = None):
    if keyword == None:
        return {"Error": "enter a keyword"}
    link = f'https://mangapanda.in/search?q={keyword}'
    r = requests.get(link).text
    soup = bs(r, "lxml")
    manga_results = soup.find_all("a", class_="tooltips")
    manga_ind = 0
    for i in manga_results:
        manga = {}
        manga["title"] = i["title"]
        manga["cover"] = i.find("img")["src"]
        ln = requests.get(i.get("href")).text
        soup = bs(ln, 'lxml')
        chapters = soup.find_all('li', class_='row')
        ch_list = []
        for j in chapters:
            l = j.find('a')
            l = l.get('href')
            ch_list.append(l)
        manga["chapters"] = ch_list

        manga_res[manga_ind] = manga
        manga_ind += 1
    print(manga_res)


search("jujutsu")
# get_chapters("https://mangapanda.in/baki-dou-2018-chapter-3")
# ch = get_manga("baki-dou-2018")
# get_chapters(ch)
