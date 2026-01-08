import time
import requests
from release_sentinel.checks.result import CheckResult, OK, CRIT

RETRYABLE = {429, 500, 502, 503, 504}

def check_api(url: str, timeout=3, retries=3) -> CheckResult:
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                return CheckResult(OK, f"API OK: {url}")

            if r.status_code in RETRYABLE:
                raise RuntimeError(f"Retryable {r.status_code}")

            return CheckResult(
                CRIT,
                f"API CRITICAL: {url} returned {r.status_code}"
            )

        except Exception:
            if attempt == retries - 1:
                return CheckResult(
                    CRIT,
                    f"API CRITICAL: {url} unreachable"
                )
            time.sleep(2 ** attempt)
