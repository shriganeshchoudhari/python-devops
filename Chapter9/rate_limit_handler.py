import requests
import time

def rate_limit_handler(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "1"))
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            # Retry once
            response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    resp = rate_limit_handler("https://httpbin.org/status/429")
    if resp:
        print("Final status:", resp.status_code)