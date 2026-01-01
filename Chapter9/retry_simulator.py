import requests
import time

def get_with_retry(url, retries=3, timeout=5):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            last_error = e
            time.sleep(1)  # small delay before retry
    # If all retries exhausted
    raise RuntimeError(f"Failed after {retries} retries") from last_error


if __name__ == "__main__":
    try:
        resp = get_with_retry("https://api.github.com")
        print("Success:", resp.status_code)
    except Exception as e:
        print("Final error:", e)