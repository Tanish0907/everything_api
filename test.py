import requests
from bs4 import BeautifulSoup as bs


def get_anime_info(anime_name: str):
    link = f"https://gogoanimehd.to/category/{anime_name}"
    r = requests.get(link).text
    soup = bs(r, 'lxml')
    total_ep = soup.find('ul', {'id': 'episode_page'})
    total_ep = total_ep.find("a")['ep_end']
    total_ep = int(total_ep)
    anime_details = soup.find_all("p", class_="type")
    genre = []
    for i in anime_details[2].find_all("a"):
        genre.append(i["title"])
    print(genre)


get_anime_info("jujutsu-kaisen-2nd-season-dub")
