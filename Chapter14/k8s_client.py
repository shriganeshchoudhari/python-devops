import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_clients():
    try:
        config.load_kube_config()
        return client.CoreV1Api(), client.AppsV1Api()
    except Exception as e:
        logger.error("Failed to load kubeconfig: %s", e)
        raise
