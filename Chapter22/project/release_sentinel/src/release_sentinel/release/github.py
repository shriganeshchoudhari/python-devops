import os
import logging
import requests

logger = logging.getLogger(__name__)

def create_github_release(version: str):
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")

    if not token or not repo:
        raise RuntimeError("GitHub credentials not configured")

    url = f"https://api.github.com/repos/{repo}/releases"

    payload = {
        "tag_name": version,
        "name": version,
        "body": f"Automated release {version}",
        "draft": False,
        "prerelease": False
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=5
    )

    if r.status_code not in (201,):
        raise RuntimeError(
            f"GitHub release failed: {r.status_code} {r.text}"
        )

    logger.info("GitHub release %s created", version)
