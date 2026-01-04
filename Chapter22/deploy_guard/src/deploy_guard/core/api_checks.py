import logging, time, requests
log = logging.getLogger("deploy_guard.api")

def get_with_retry(url, max_attempts=3, timeout=5):
    backoff = 1
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code >= 500:
                raise requests.exceptions.RequestException(f"5xx {r.status_code}")
            log.info("API check succeeded on attempt %d: %s", attempt, r.status_code)
            return 0
        except requests.exceptions.RequestException as e:
            if attempt == max_attempts:
                log.error("Final failure after %d attempts: %s", attempt, e)
                return 2
            log.warning("Attempt %d failed: %s. Retrying in %d seconds...", attempt, e, backoff)
            time.sleep(backoff)
            backoff *= 2