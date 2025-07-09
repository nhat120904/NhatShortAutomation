# import requests

# response = requests.get("https://api.animechan.io/v1/quotes/random")

# if response.status_code == 200:
#     data = response.json()
#     if data.get("status") == "success":
#         quote = data["data"]
#         print("Quote:", quote["content"])
#         print("Anime:", quote["anime"]["name"], f"({quote['anime']['altName']})")
#         print("Character:", quote["character"]["name"])
#     else:
#         print("Failed to retrieve quote: ", data)
# else:
#     print("HTTP Error:", response.status_code)


# import requests

# def get_random_quote(anime):
#     url = f"https://api.animechan.io/v1/quotes/random/anime?title={anime}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return f"{data['quote']} - {data['character']}"
#     else:
#         return "Failed to retrieve quote"

# # Get and print a random quote from Kimetsu no Yaiba
# anime_name = "Kimetsu no Yaiba"
# random_quote = get_random_quote(anime_name)
# print(random_quote)

import requests
from urllib.parse import quote  # makes the anime name URL-safe

BASE_URL = "https://api.animechan.io/v1"

def get_random_quote(anime: str = "Kimetsu no Yaiba") -> dict:
    """
    Fetch a single random quote for the given anime.

    Returns a dict with keys: anime, character, quote.
    Raises SystemExit on network errors and ValueError on API-level errors.
    """
    url = f"{BASE_URL}/quotes/random?anime={quote(anime)}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()                # HTTP-level problems
    except requests.RequestException as exc:
        raise SystemExit(f"Network error: {exc}") from exc

    payload = resp.json()
    if payload.get("status") != "success":     # API-level problems
        raise ValueError(f"Unexpected API response: {payload}")

    data = payload["data"]                     # structure shown in docs
    return {
        "anime":     data["anime"]["name"],
        "character": data["character"]["name"],
        "quote":     data["content"],
    }

# Demo
if __name__ == "__main__":
    anime = "Kimetsu no Yaiba"
    q = get_random_quote(anime)
    print(f'"{q["quote"]}" — {q["character"]} ({q["anime"]})')
