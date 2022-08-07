from re import A
import socket
import os

PORT = 2820
USERNAME = "_"
PASSWORD = "_"
LOGGED_IN = False 
MENU = []
PROMPT = "\nEnter menu item number: "


def run() -> None:
    init_menus()
    while not login():
        print("Login failed. Please retry")
    print("Login successfull")
    _ = input("\nPress enter to continue")
    command = generate_command()
    print(command)
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
        _ = input("\nPress enter to continue")
        command = generate_command()
        print(command)


def init_menus():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', PORT))
    client.send("help".encode())
    response = client.recv(1024).decode()
    entries = response.split('\n')
    entries = [e.split(' ') for e in entries]
    global MENU
    MENU = [(e[0], e[1:]) for e in entries]
    

def print_menu() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    for idx, entry in enumerate(MENU):
        print(f"{idx+1}-{entry[0]}")


def get_command_parameters(parameters: list) -> list:
    return [input(f"{parameter}: ") for parameter in parameters]


def generate_command() -> str:
    print_menu()
    action = input(PROMPT)
    try:
        action = int(action) - 1
    except:
        return action
    params_value = []
    for param in MENU[action][1]:
        if not MENU[action][0].startswith("register"):
            if param == "username":
                params_value.append(USERNAME)
            elif param == "password":
                params_value.append(PASSWORD)
        else:
            params_value.append(input(f"{param}: "))
    return f"{MENU[action][0]} {USERNAME} {PASSWORD} {' '.join(params_value)}"


def login() -> bool:
    print("1-Login\n2-Continue as a guest")
    login = input(PROMPT) == "1"
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
            global LOGGED_IN
            USERNAME = username
            PASSWORD = password
            LOGGED_IN = True
            return True
        return False
    return True


def logout() -> None:
    global USERNAME
    global PASSWORD
    global LOGGED_IN
    USERNAME = "_"
    PASSWORD = "_"
    LOGGED_IN = False


if __name__ == '__main__':
    run()
