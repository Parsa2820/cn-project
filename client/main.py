import socket

PORT = 2820


def run() -> None:
    command = input(">> ")
    while command != "exit":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', PORT))
        client.send(command.encode())
        response = client.recv(1024).decode()
        print(response)
        client.close()
        command = input(">> ")


if __name__ == '__main__':
    run()
