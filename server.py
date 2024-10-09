import time
import paramiko

from constansts import CMD_DICT


def get_client(hostname: str, username: str, timeout: int = 5) -> paramiko.SSHClient:
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, timeout=timeout)
    return ssh


def get_client_list(
    hostname_list: list[str], username: str
) -> list[paramiko.SSHClient]:
    client_list = []
    for hostname in hostname_list:
        try:
            ssh = get_client(hostname, username)
            client_list.append(ssh)
        except:
            print(f"Unable to connect to {hostname}")
            continue

    return client_list


def get_server_usernames(ssh: paramiko.SSHClient) -> list:
    stdin, stdout, stderr = ssh.exec_command(CMD_DICT["get_users"])
    return stdout.read().decode().split()


def get_server_processes_per_user(ssh: paramiko.SSHClient, username: str) -> list:
    stdin, stdout, stderr = ssh.exec_command(f"ps -u {username}")
    raw_psout = stdout.read().decode()

    processes = []
    for process in raw_psout.split("\n")[1:]:
        if not process:
            break

        id, tty, time, cmd = process.split()
        processes.append((id, time, cmd))

    return processes


def is_process_running(ssh: paramiko.SSHClient, p: str):
    stdin, stdout, stderr = ssh.exec_command(f"ps")
    raw_psout = stdout.read().decode()

    for process in raw_psout.split("\n")[1:]:
        if not process:
            break

        id, tty, time, cmd = process.split()
        if cmd == p:
            return True

    return False


def is_server_available(ssh: paramiko.SSHClient, current_username: str):
    for username in get_server_usernames(ssh):
        processes = get_server_processes_per_user(ssh, username)

        if username == current_username:
            if bool([p for _, _, p in processes if p == "abako"]):
                return False
            continue

        if processes:
            return False

    return True


def wait_for_process_to_end(ssh: paramiko.SSHClient, p: str, wait_time: int = 120):
    while is_process_running(ssh, p):
        time.sleep(wait_time)
