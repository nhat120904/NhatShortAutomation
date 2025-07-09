import requests
 
res = requests.get("https://api.nekosapi.com/v4/images")
res.raise_for_status()
 
data = res.json()
print(data)