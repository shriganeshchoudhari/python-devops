import requests

response = requests.get("https://api.github.com")
print(response.status_code)

print(response.text)

print(response.headers) 