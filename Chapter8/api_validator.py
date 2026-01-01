import requests

def check_api(url: str):
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception(f"API call failed with status {response.status_code}")
    return response.json()

# Example usage
if __name__ == "__main__":
    try:
        data = check_api("https://api.github.com")
        print("API OK, got keys:", list(data.keys())[:5])  # show first 5 keys
    except Exception as e:
        print("Error:", e)