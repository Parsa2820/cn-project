import socket
import os
import cv2
import socket
import numpy as np
import time
import base64
import pyaudio
import pickle
import struct
import tqdm

ADDRESS = 'localhost'
PORT = 2820
USERNAME = "_"
PASSWORD = "_"
LOGGED_IN = False
MENU = []
PROMPT = "\nEnter menu item number (or type logout/exit): "


def run() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    while not login():
        print("Login failed. Please retry")
    print("Login successfull")
    _ = input("\nPress enter to continue")
    command = ""
    while command != "exit":
        command = generate_command()
        print(command)
        if command == "logout":
            logout()
            run()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', PORT))
        client.send(command.encode())
        response = client.recv(1024).decode()
        print(response.replace("%20", " "))
        client.close()
        if command.startswith("upload_video"):
            send_data(int(response.strip()), input("Enter file path: "))
        if command.startswith("watch_video"):
            video_port, audio_port = map(int, response.split(' '))
            watch_video(video_port, audio_port)
        _ = input("\nPress enter to continue")


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


def read_param(param: str) -> str:
    return input(f"{param}: ").replace(" ", "%20")


def generate_command() -> str:
    print_menu()
    action = input(PROMPT)
    try:
        action = int(action) - 1
    except:
        return action
    params_value = []
    for param in MENU[action][1]:
        if MENU[action][0].startswith("register") or MENU[action][0].startswith("login"):
            params_value.append(read_param(param))
        else:
            if param == "username":
                params_value.append(USERNAME)
            elif param == "password":
                params_value.append(PASSWORD)
            else:
                params_value.append(read_param(param))
    return f"{MENU[action][0]} {USERNAME} {PASSWORD} {' '.join(params_value)}"


def login() -> bool:
    print("1-Login\n2-Continue as a guest")
    login = input(
        "Enter item number (other inputs threated as second item): ") == "1"
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


def watch_video(video_port: int, audio_port: int):
    BUFF_SIZE = 65536
    BREAK = False
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    message = b'Hello'
    client_socket.sendto(message, (ADDRESS, video_port))

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(audio_stream, ADDRESS, audio_port, BREAK)
        executor.submit(video_stream, client_socket, BUFF_SIZE)


def video_stream(client_socket, BUFF_SIZE):
    cv2.namedWindow('RECEIVING VIDEO')
    cv2.moveWindow('RECEIVING VIDEO', 10, 360)
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    while True:
        packet, _ = client_socket.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet, ' /')
        npdata = np.fromstring(data, dtype=np.uint8)

        frame = cv2.imdecode(npdata, 1)
        frame = cv2.putText(frame, 'FPS: '+str(fps), (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            client_socket.close()
            os._exit(1)
            break

        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1
    client_socket.close()
    cv2.destroyAllWindows()


def audio_stream(host_ip, port, BREAK):

    p = pyaudio.PyAudio()
    CHUNK = 1024
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=44100,
                    output=True,
                    frames_per_buffer=CHUNK)

    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port)
    print('server listening at', socket_address)
    client_socket.connect(socket_address)
    print("CLIENT CONNECTED TO", socket_address)
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)  # 4K
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            stream.write(frame)

        except:

            break

    client_socket.close()
    print('Audio closed', BREAK)


# use this after connecting to server socket!
def send_data(port: int, file_path: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port))
    f = open(file_path, 'rb')
    file_size = os.path.getsize(file_path)
    if file_size > 50_000_000:
        print("File size is too big")
        return
    l = f.read(1024)
    print('Uploading video...')
    for _ in tqdm.tqdm(range(0, file_size, 1024)):
        s.send(l)
        l = f.read(1024)
    f.close()
    s.close()
    print("File Uploaded Successfully!")


if __name__ == '__main__':
    init_menus()
    run()
