import processor
import socket
import threading
import logging
from datahandler.datahandler import DataHandler

PORT = 2820
TRUSTED_PROXIES = [
    "127.0.0.1",
]
REQUEST_COUNT_BY_ADDRESS = {}
DDOS_TIME_WINDOW_SECONDS = 10
DDOS_THRESHOLD = 10
DDOS_BLACKLIST = []


def run() -> None:
    datahandler = DataHandler("server/test_data", False)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', PORT))
    server.listen(5)
    logging.info(f"Listening on port {PORT}")
    threading.Thread(target=listen, args=(
        datahandler, server), daemon=True).start()
    threading.Timer(DDOS_TIME_WINDOW_SECONDS, clear_ddos_blacklist).start()
    while True:
        try:
            _ = input()
        except KeyboardInterrupt:
            logging.info("Shutting down...")
            server.close()
            exit()


def clear_ddos_blacklist() -> None:
    global DDOS_BLACKLIST
    DDOS_BLACKLIST = []
    threading.Timer(DDOS_TIME_WINDOW_SECONDS, clear_ddos_blacklist).start()


def listen(datahandler: DataHandler, server: socket.socket) -> None:
    while True:
        client, address = server.accept()
        logging.info(f"Accepted connection from {address}")
        if address[0] in DDOS_BLACKLIST and address[0] not in TRUSTED_PROXIES:
            logging.info(
                f"{address} is in the DDOS blacklist, closing connection")
            client.close()
            continue
        detect_ddos(address)
        threading.Thread(target=handle, args=(
            datahandler, client, address), daemon=True).start()


def detect_ddos(address: tuple) -> None:
    if address[0] in REQUEST_COUNT_BY_ADDRESS:
        REQUEST_COUNT_BY_ADDRESS[address[0]] += 1
    else:
        REQUEST_COUNT_BY_ADDRESS[address[0]] = 1
    if REQUEST_COUNT_BY_ADDRESS[address[0]] > DDOS_THRESHOLD:
        DDOS_BLACKLIST.append(address[0])


def handle(datahandler: DataHandler, client: socket.socket, address: tuple) -> None:
    command = client.recv(1024).decode()
    logging.info(f"Received command: {command} from {address}")
    if check_proxy_for_admin(datahandler, client, address, command):
        response = processor.process(datahandler, command)
    else:
        response = "You are admin, but you are not connected through the proxy!"
        logging.error(response + " from " + str(address))
    logging.info(f"Sending response: {response} to {address}")
    client.send(response.encode())
    logging.info(f"Closing connection to {address}")
    client.close()


def check_proxy_for_admin(datahandler: DataHandler, client: socket.socket, address: tuple, command: str) -> bool:
    try:
        username = command.split(" ")[1]
        account = datahandler.get_account_by_username(username)
    except:
        return True
    if account.account_type == "admin" or account.account_type == "manager":
        return address[0] in TRUSTED_PROXIES
    return True
