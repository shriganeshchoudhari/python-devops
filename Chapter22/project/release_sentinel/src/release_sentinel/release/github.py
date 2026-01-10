import os
import logging
import requests

logger = logging.getLogger(__name__)


def create_github_release(version: str, body: str):
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")

    if not token or not repo:
        raise RuntimeError("GitHub credentials not configured")

    url = f"https://api.github.com/repos/{repo}/releases"

    payload = {
        "tag_name": version,
        "name": version,
        "body": body,
        "draft": False,
        "prerelease": False
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=5
    )

    if response.status_code != 201:
        raise RuntimeError(
            f"GitHub release failed: {response.status_code} {response.text}"
        )

    logger.info("GitHub release %s created successfully", version)
