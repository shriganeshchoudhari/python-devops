def run_remote(host, user, command, key_file, timeout=10):
    """
    Safe SSH wrapper:
    - Key-based auth only
    - Timeout enforced
    - Exit code checked
    - Logs everything
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, key_filename=key_file, timeout=timeout)

        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()

        if exit_code == 0:
            logger.info("Command succeeded: %s", stdout.read().decode().strip())
        else:
            logger.error("Command failed (%d): %s", exit_code, stderr.read().decode().strip())

        client.close()
        return exit_code
    except Exception as e:
        logger.error("SSH error: %s", e)
        return 1