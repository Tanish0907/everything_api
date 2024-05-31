import requests
url="http://localhost:8000"
def fetch(term:str)->dict:
    results=requests.get(f"{url}/manga/search?term={term}").json()
    return results
def fetch_book(name:str)->dict:
    results=requests.get(f"{url}/manga/{name}").json()
    print(results)
    return results
