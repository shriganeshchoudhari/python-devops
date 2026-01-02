import os

def remote_file_fetch(host, user, key_file, remote_path, local_path, timeout=10):
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=user, key_filename=key_file)
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.get(remote_path, local_path)
        sftp.close()
        transport.close()

        if os.path.exists(local_path):
            logger.info("File fetched successfully: %s", local_path)
            return 0
        else:
            logger.error("File fetch failed: %s", local_path)
            return 1
    except Exception as e:
        logger.error("SFTP error: %s", e)
        return 1
    