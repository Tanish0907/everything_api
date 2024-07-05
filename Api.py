from socket import timeout
from typing import Optional
from fastapi import FastAPI, Query
from Torrent import Search
from Manga import Mangasearch, Get_manga
from Comic import Comicsearch, Get_comic
from fastapi.middleware.cors import CORSMiddleware

# caching #######################################################################################################
import functools
import time


def timedlru_cache(maxsize=128, timeout=None):
    cache = {}

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))  # Create a hashable key
            if key in cache:
                timestamp, value = cache[key]
                if timeout is None or time.time() - timestamp <= timeout:
                    return value  # Return cached value if not expired

            value = func(*args, **kwargs)
            cache[key] = (time.time(), value)  # Cache the value with current timestamp
            return value

        return wrapper

    return decorator


##################################################################################################################

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your needs. "*" allows all origins.
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ],  # Adjust the allowed methods as needed.
    allow_headers=["*"],  # Adjust the allowed headers as needed.
)


@app.get("/")
@timedlru_cache(maxsize=10, timeout=600)
def index():
    return "api is up!!"


@app.get("/manga/search")
#@timedlru_cache(maxsize=10, timeout=600)
def manga_search(term: str):
    res = Mangasearch(term)
    return res


@app.get("/manga/{manga_name}")
#@timedlru_cache(maxsize=10, timeout=600)
def manga(
    manga_name: str, source: str = Query("mangapanda", enum=["mangapanda", "rmanga"])
):
    res = Get_manga(manga_name, source)
    return res


@app.get("/comic/search")
#@timedlru_cache(maxsize=10, timeout=10)
def comic_search(term: str):
    res = Comicsearch(term)
    return res


@app.get("/comic/{comic_name}")
#@timedlru_cache(maxsize=10, timeout=600)
def comic(comic_name: str):
    res = Get_comic(comic_name)
    return res


@app.get("/torr/search")
#@timedlru_cache(maxsize=10, timeout=600)
def torr_search(term: str, catagory: Optional[str] = None):
    res = Search(term, catagory)
    return res
