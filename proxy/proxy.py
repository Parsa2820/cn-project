import json
import socket
import threading


SERVER_PORT = 2820
PROXY_PORT = 5850


def check_user(username: str, password: str) -> bool:
    for user in USERS:
        if user['username'] == username and user['password'] == password:
            return True
    return False


def handle(client: socket.socket, address: tuple) -> None:
    command = client.recv(1024).decode()
    splitted_command = command.split(" ")
    proxy_username = splitted_command[0]
    proxy_password = splitted_command[1]
    if check_user(proxy_username, proxy_password):
        proxy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_client.connect((SERVER, SERVER_PORT))
        proxy_client.send(" ".join(splitted_command[2:]))
        response = proxy_client.recv(1024).decode()
        proxy_client.close()
        client.send(response.encode())
    else:
        client.send("Invalid credentials for proxy".encode())
    client.close()


def listen(server: socket.socket) -> None:
    while True:
        client, address = server.accept()
        threading.Thread(target=handle, args=(
            client, address), daemon=True).start()


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PROXY_PORT))
    server.listen(5)
    threading.Thread(target=listen, args=(server, ), daemon=True).start()
    while True:
        try:
            _ = input()
        except KeyboardInterrupt:
            server.close()
            exit()


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    SERVER = config["server"]
    USERS = config["users"]
    main()
