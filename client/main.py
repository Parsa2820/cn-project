import socket

PORT = 2820
USERNAME = "_"
PASSWORD = "_"


def run() -> None:
    while not login():
        print("Login failed. Please retry")
    print("Login successfull")
    command = input(">> ")
    while command != "exit":
        if command == "logout":
            logout()
            run()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', PORT))
        client.send(command.encode())
        response = client.recv(1024).decode()
        print(response)
        client.close()
        command = input(">> ")


def login() -> bool:
    print("1-Login\n2-Continue as a guest")
    login = input() == "1"
    if login:
        username = input("Username: ")
        password = input("Password: ")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', PORT))
        client.send(f"login _ _ {username} {password}".encode())
        response = client.recv(1024).decode()
        client.close()
        if "success" in response:
            global USERNAME
            global PASSWORD
            USERNAME = username
            PASSWORD = password
            return True
        return False
    return True


def logout() -> None:
    global USERNAME
    global PASSWORD
    USERNAME = "_"
    PASSWORD = "_"


if __name__ == '__main__':
    run()
