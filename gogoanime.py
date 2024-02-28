from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse
import json
import requests


class GogoCDN:
    serverName = "goload"
    sources = []

    keys = {
        "key": b"37911490979715163134003223491201",
        "secondKey": b"54674138327930866480207815084989",
        "iv": b"3134003223491201",
    }
    referer = ""

    def __init__(self, session):
        self.session = session
        self.session.headers["User-Agent"] = "Mozilla/5.0"

    def extract(self, video_url):
        self.referer = video_url

        res = self.session.get(video_url)
        soup = BeautifulSoup(res.text, "html.parser")
        my_id = video_url.split("id=")[1].split("&")[0]
        encrypted_params = self.generate_encrypted_ajax_params(soup, my_id)
        parsedUrl = urlparse(video_url)

        self.session.headers["X-Requested-With"] = "XMLHttpRequest"
        encrypted_data = self.session.get(
            f"{parsedUrl.scheme}://{parsedUrl.netloc}/encrypt-ajax.php?{encrypted_params}"
        )
        data = encrypted_data.text
        json_data = json.loads(data)
        decrypted_data = self.decrypt_ajax_data(json_data.get("data"))
        self.session.headers["X-Requested-With"] = ""

        if "source" not in decrypted_data or not decrypted_data.get("source"):
            raise Exception("No source found. Try a different server.")
        my_data: str = decrypted_data.get("source")[0].get("file")
        if ".m3u8" in my_data:
            resResult = self.session.get(my_data)
            pattern = r'#EXT-X-STREAM-INF:PROGRAM-ID=\d+,BANDWIDTH=\d+,(RESOLUTION=[^,]+,NAME="[^"]+")\s+(\S+)'
            matches = re.findall(pattern, resResult.text)
            resolutions = [f"{match[0]}\n{match[1]}" for match in matches]
            print(resolutions)
            for res in resolutions:
                index = len(my_data) - my_data[::-1].index("/") - 1
                quality = res.split("\n")[0].split("x")[1].split(",")[0]
                url = my_data[:index]
                self.sources.append(
                    {
                        "url": url + "/" + res.split("\n").pop(),
                        "isM3U8": ".m3u8" in url + "/" + res.split("\n").pop(),
                        "quality": quality + "p",
                    }
                )
            for source in decrypted_data.get("source", []):
                self.sources.append(
                    {
                        "url": source.get("file"),
                        "isM3U8": ".m3u8" in source.get("file"),
                        "quality": "default",
                    }
                )
        else:
            for source in decrypted_data.get("source", []):
                self.sources.append(
                    {
                        "url": source.get("file"),
                        "isM3U8": ".m3u8" in source.get("file"),
                        "quality": source.get("label").split(" ")[0] + "p",
                    }
                )
        for source in decrypted_data.get("source_bk", []):
            self.sources.append(
                {
                    "url": source.get("file"),
                    "isM3U8": ".m3u8" in source.get("file"),
                    "quality": "backup",
                }
            )
        return self.sources

    def encrypt_data(self, data):
        cipher = AES.new(self.keys["key"], AES.MODE_CBC, self.keys["iv"])
        encrypted_data = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
        encrypted_key = base64.b64encode(encrypted_data).decode("utf-8")
        return encrypted_key

    def decrypt_data(self, data):
        cipher = AES.new(self.keys["key"], AES.MODE_CBC, self.keys["iv"])
        data_bytes = base64.b64decode(data)
        decrypted_data = unpad(cipher.decrypt(data_bytes), AES.block_size)
        return decrypted_data.decode("utf-8")

    def generate_encrypted_ajax_params(self, soup, id):
        encrypted_key = self.encrypt_data(id)
        script_value = soup.find("script", {"data-name": "episode"})["data-value"]
        decrypted_token = self.decrypt_data(script_value)
        return f"id={encrypted_key}&alias={id}&{decrypted_token}"

    def decrypt_ajax_data(self, encrypted_data):
        cipher = AES.new(self.keys["secondKey"], AES.MODE_CBC, self.keys["iv"])
        encrypted_data_bytes = base64.b64decode(encrypted_data)
        decrypted_data = unpad(cipher.decrypt(encrypted_data_bytes), AES.block_size)
        decrypted_data_str = decrypted_data.decode("utf-8")
        return json.loads(decrypted_data_str)


class GogoAnime:
    BASE_URL = "https://gogoanime3.co/"
    ajaxUrl = "https://ajax.gogo-load.com/ajax"

    def __init__(self, session) -> None:
        self.session = session
        self.session.headers["User-Agent"] = "Mozilla/5.0"

    def search(self, query: str, page: int = 1):
        """Used to Scrape Search Results from Gogoanime

        Args:
            query (str): Search Query
            page (int, optional): Page Number. Defaults to 1.

        Returns:
            _type_: _description_
        """
        searchResult = {"currentPage": page, "hasNextPage": False, "results": []}
        res = self.session.get(
            f"{self.BASE_URL}/search.html?keyword={query}&page={page}",
        )
        soup = BeautifulSoup(res.text, "html.parser")
        selected_li = soup.select(
            "div.anime_name.new_series > div > div > ul > li.selected"
        )
        if selected_li:
            searchResult["hasNextPage"] = bool(selected_li[0].find_next_sibling())
        anime_list = soup.select("div.last_episodes > ul > li")
        for el in anime_list:
            elem = el.find("p", class_="name").find("a")
            result = {
                "id": elem.get("href").split("/").pop(),
                "title": elem.get("title"),
                "url": f"{self.BASE_URL}/{elem.get('href')}",
                "image": el.find("div").find("a").find("img").get("src"),
                "releaseDate": el.find("p", class_="released").get_text().strip(),
                "subOrDub": "dub" if "dub" in elem.get_text().lower() else "sub",
            }
            searchResult["results"].append(result)

        return searchResult

    def fetchAnimeInfo(self, anime_id: str):
        if "gogoanime" not in anime_id:
            anime_id = f"{self.BASE_URL}/category/{anime_id}"
        anime_info = {
            "id": "",
            "title": "",
            "url": "",
            "genres": [],
            "totalEpisodes": 0,
        }
        res = self.session.get(anime_id)
        soup = BeautifulSoup(res.text, "html.parser")
        anime_info["id"] = anime_id.split("/").pop()
        title_elem = soup.select_one(
            "section.content_left > div.main_body > div:nth-child(2) > div.anime_info_body_bg > h1"
        )
        anime_info["title"] = title_elem.getText().strip() if title_elem else ""
        anime_info["url"] = anime_id
        anime_info["image"] = soup.select_one("div.anime_info_body_bg > img").get("src")
        anime_info["releaseDate"] = (
            soup.select_one("div.anime_info_body_bg > p:nth-child(7)")
            .getText()
            .strip()
            .split("Released: ")
            .pop()
        )
        anime_info["description"] = (
            soup.select_one("div.anime_info_body_bg > p:nth-child(5)")
            .getText()
            .strip()
            .replace("Plot Summary: ", "")
        )
        anime_info["subOrDub"] = (
            "dub" if "dub" in anime_info["title"].lower() else "sub"
        )
        anime_info["type"] = (
            soup.select_one("div.anime_info_body_bg > p:nth-child(4) > a")
            .getText()
            .strip()
            .upper()
        )
        # anime_info["status"] = "Unknown"
        # status = (
        #     soup.select_one("div.anime_info_body_bg > p:nth-child(8) > a")
        #     .getText()
        #     .strip()
        # )
        # if status == "Ongoing":
        #     anime_info["status"] = "Ongoing"
        # elif status == "Completed":
        #     anime_info["status"] = "Completed"
        # elif status == "Upcoming":
        #     anime_info["status"] = "Upcoming"
        anime_info["otherName"] = (
            soup.select_one("div.anime_info_body_bg > p:nth-child(9)")
            .getText()
            .replace("Other name: ", "")
            .replace(";", ",")
        )
        for genre in soup.select("div.anime_info_body_bg > p:nth-child(6) > a"):
            anime_info["genres"].append(genre.get("title"))
        ep_start = soup.select_one("#episode_page > li a").get("ep_start")
        last_li = soup.select_one("#episode_page > li:last-child")
        if isinstance(last_li, Tag):
            ep_end = last_li.select_one("a")["ep_end"]
        else:
            ep_end = None
        movie_id = soup.select_one("#movie_id").get("value")
        alias = soup.select_one("#alias_anime").get("value")

        res2 = self.session.get(
            f"{self.ajaxUrl}/load-list-episode?ep_start={ep_start}&ep_end={ep_end}&id={movie_id}&default_ep=${0}&alias={alias}"
        )
        soup2 = BeautifulSoup(res2.text, "html.parser")
        anime_info["episodes"] = []
        for ep in soup2.select("#episode_related > li"):
            elem = {
                "id": ep.find("a").get("href").split("/").pop(),
                "number": int(ep.select_one("div.name").getText().replace("EP", "")),
                "url": f"{self.BASE_URL}/{ep.find('a').get('href').strip()}",
            }
            anime_info["episodes"].append(elem)
        anime_info["episodes"].reverse()
        anime_info["totalEpisodes"] = int(ep_end) if ep_end else 0
        return anime_info

    def fetchEpisodeSources(self, episode_id: str):
        if not str(episode_id).startswith("http"):
            res = self.session.get(f"{self.BASE_URL}/{episode_id}")
            soup = BeautifulSoup(res.text, "html.parser")
            serverUrl = ""
            serverUrl = soup.select_one(
                "div.anime_video_body > div.anime_muti_link > ul > li.vidcdn > a"
            ).get("data-video")
            return self.fetchEpisodeSources(serverUrl)
        serverUrl = episode_id
        return {
            "headers": {"Referer": serverUrl},
            "sources": GogoCDN(session=self.session).extract(serverUrl),
            "download": f"https://gogohd.net/download?{serverUrl.split('?').pop()}",
        }
