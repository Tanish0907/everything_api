import requests
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool as ThreadPool


class Anime:
    def __init__(self, anime_name):
        self.animename = anime_name.replace(" ", "%20")
        self.anime_list = {}
        self.ep_list = []
        self.download_links = []
        self.anime_selected = {}
        self.scraped_ep_win = []

    def search(self, anime_name: str = None):
        if anime_name == None:
            anime_name = self.animename
        self.anime_list.clear()
        link = f"https://anitaku.to/search.html?keyword={anime_name}"
        r = requests.get(link).content
        soup = bs(r, "lxml")
        search_res = soup.find("ul", class_="items")
        links = search_res.find_all("a")
        for i in links:
            self.anime_list[
                i.get("href").split("/")[-1]
            ] = f"https://anitaku.to{i.get('href')}"
        return self.anime_list

    def get_anime(self, selected_anime: str):
        self.anime_selected.clear()
        self.search(selected_anime)
        link = self.anime_list[selected_anime]
        print(link)
        r = requests.get(link).content
        soup = bs(r, "lxml")
        total_ep = soup.find("ul", {"id": "episode_page"})
        total_ep = total_ep.find("a")["ep_end"]
        total_ep = int(total_ep)
        link = link.replace("category/", "")
        for i in range(1, total_ep + 1):
            x = str(i)
            self.ep_list.append(f"{link}-episode-{x}")
        print(self.ep_list)
        pool = ThreadPool(10)
        pool.map(self.scrape_episode_window, self.ep_list)
        print(pool.close())
        print(pool.join())
        return self.scraped_ep_win

    def scrape_episode_window(self, link):
        r = requests.get(link).text
        soup = bs(r, "lxml")
        soup = soup.find("div", class_="play-video")
        soup = soup.find("iframe")
        self.scraped_ep_win.append(soup["src"])
        # print(self.scraped_ep_win)

    def get_download_link(self):
        for i in self.ep_list:
            r = requests.get(i).text
            soup = bs(r, "lxml")
            download_link = soup.find("li", class_="dowloads")
            download_link = download_link.find("a").get("href")
            # print(download_link)
            self.download_links.append(download_link)
        return self.download_links
