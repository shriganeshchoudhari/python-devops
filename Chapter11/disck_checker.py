def remote_disk_check(host, user, key_file, threshold=80, timeout=10):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, key_filename=key_file, timeout=timeout)

        stdin, stdout, stderr = client.exec_command("df -h /")
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode().splitlines()

        if exit_code == 0 and len(output) > 1:
            # Parse usage percentage from second line
            usage = output[1].split()[4]  # e.g. "45%"
            percent = int(usage.strip('%'))
            logger.info("Disk usage: %d%%", percent)
            client.close()
            if percent > threshold:
                logger.error("Disk usage above threshold")
                sys.exit(1)
            else:
                sys.exit(0)
        else:
            logger.error("Disk check failed: %s", stderr.read().decode().strip())
            client.close()
            sys.exit(exit_code)
    except Exception as e:
        logger.error("Connection error: %s", e)
        sys.exit(1)
        