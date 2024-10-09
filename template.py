from server import get_client, is_server_available


def main() -> None:
    USERNAME = "aridai"
    ssh = get_client("revolver", USERNAME)

    if not is_server_available(ssh, USERNAME):
        return

    # ssh.exec_commands(...)

    ssh.close()


if __name__ == "__main__":
    main()
