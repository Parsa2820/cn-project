import processor
import socket
import threading
import logging
from datahandler.datahandler import DataHandler

PORT = 2820
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)s: %(message)s')


def run() -> None:
    datahandler = DataHandler("../data", True)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', PORT))
    server.listen(5)
    logging.info(f"Listening on port {PORT}")
    threading.Thread(target=listen, args=(
        datahandler, server), daemon=True).start()
    while True:
        try:
            _ = input()
        except KeyboardInterrupt:
            logging.info("Shutting down...")
            server.close()
            exit()


def listen(datahandler: DataHandler, server: socket.socket) -> None:
    while True:
        client, address = server.accept()
        logging.info(f"Accepted connection from {address}")
        threading.Thread(target=handle, args=(
            datahandler, client, address), daemon=True).start()


def handle(datahandler: DataHandler, client: socket.socket, address: tuple) -> None:
    command = client.recv(1024).decode()
    logging.info(f"Received command: {command} from {address}")
    response = processor.process(datahandler, command)
    logging.info(f"Sending response: {response} to {address}")
    client.send(response.encode())
    logging.info(f"Closing connection to {address}")
    client.close()
