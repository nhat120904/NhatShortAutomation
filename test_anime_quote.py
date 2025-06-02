import requests

response = requests.get('https://api.animechan.io/v1/quotes/random')

if response.status_code == 200:
    data = response.json()
    if data.get('status') == 'success':
        quote = data['data']
        print("Quote:", quote['content'])
        print("Anime:", quote['anime']['name'], f"({quote['anime']['altName']})")
        print("Character:", quote['character']['name'])
    else:
        print("Failed to retrieve quote: ", data)
else:
    print("HTTP Error:", response.status_code)