import requests

ALLANIME_REF = "https://allanime.to"
ALLANIME_BASE = "allanime.day"
ALLANIME_API = f"https://api.{ALLANIME_BASE}"
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"

def search_anime(query, translation_type):
    search_gql = '''
    query($search: SearchInput, $limit: Int, $page: Int, $translationType: VaildTranslationTypeEnumType, $countryOrigin: VaildCountryOriginEnumType) {
        shows(search: $search, limit: $limit, page: $page, translationType: $translationType, countryOrigin: $countryOrigin) {
            edges {
                _id
                name
                availableEpisodes
                __typename
            }
        }
    }'''
    
    variables = {
        "search": {
            "allowAdult": True,
            "allowUnknown": False,
            "query": query
        },
        "limit": 40,
        "page": 1,
        "translationType": translation_type,
        "countryOrigin": "ALL"
    }
    
    response = requests.post(
        f"{ALLANIME_API}/api",
        json={"query": search_gql, "variables": variables},
        headers={"User-Agent": AGENT, "Referer": ALLANIME_REF}
    )
    
    return response.json()

# Usage example:
if __name__ == "__main__":
    anime_name = "jujutsu"
    translation_type = "dub"
    result = search_anime(anime_name, translation_type)
    print(result)


