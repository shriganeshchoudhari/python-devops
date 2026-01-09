import os
import logging
import requests

logger = logging.getLogger(__name__)

def send_webhook(message: str, severity: str):
    webhook_url = os.getenv("RS_ALERT_WEBHOOK")

    if not webhook_url:
        logger.info("No webhook configured, skipping alert")
        return

    payload = {
        "text": f":rotating_light: Release Sentinel Alert\n"
                f"*Severity:* {severity}\n"
                f"*Message:* {message}"
    }

    try:
        r = requests.post(
            webhook_url,
            json=payload,
            timeout=3
        )
        r.raise_for_status()
        logger.info("Alert sent successfully")
    except Exception as e:
        # NEVER fail the pipeline because alerting failed
        logger.error("Failed to send alert: %s", e)
