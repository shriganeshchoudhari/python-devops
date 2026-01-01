import requests

def main():
    url = "https://api.github.com"
    try:
        response = requests.get(url, timeout=5)  # timeout in seconds
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            # Print one field from JSON (example: 'current_user_url')
            print("Field current_user_url:", data.get("current_user_url"))
        else:
            print("API call failed")

    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()