import paramiko
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RemoteUptime")

def remote_uptime(host, user, key_file, timeout=10):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, key_filename=key_file, timeout=timeout)

        stdin, stdout, stderr = client.exec_command("uptime")
        exit_code = stdout.channel.recv_exit_status()

        if exit_code == 0:
            logger.info("Uptime: %s", stdout.read().decode().strip())
            client.close()
            sys.exit(0)
        else:
            logger.error("Failed to run uptime: %s", stderr.read().decode().strip())
            client.close()
            sys.exit(exit_code)
    except Exception as e:
        logger.error("Connection error: %s", e)
        sys.exit(1)