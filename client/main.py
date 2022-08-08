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
import keyboard
import sys


ADDRESS = 'localhost'
PORT = 2820
PROXY_PORT = 5850
USERNAME = "_"
PASSWORD = "_"
LOGGED_IN = False
MENU = []
PROMPT = "\nEnter menu item number (or type logout/exit): "


def send_command(command: str) -> str:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if EN_PROXY:
        client.connect((PROXY_ADDRESS, PROXY_PORT))
        client.send(f"{PROXY_USERNAME} {PROXY_PASSWORD} {command}".encode())
    else:
        client.connect((ADDRESS, PORT))
        client.send(command.encode())
    response = client.recv(1024).decode()
    client.close()
    return response


def run() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    while not login():
        print("Login failed. Please retry")
    print("Login successfull")
    _ = input("\nPress enter to continue")
    command = ""
    while True:
        command = generate_command()
        print(command)
        if command == "logout":
            logout()
            run()
        elif command == "exit":
            break
        response = send_command(command)
        print(response.replace("%20", " "))
        if command.startswith("upload_video"):
            if(not response.startswith("Error")):
                send_data(int(response.strip()), input("Enter file path: "))
        if command.startswith("watch_video"):
            if (not response.startswith("Error")):
                video_port, audio_port = map(int, response.split(' '))
                watch_video(video_port, audio_port)
        _ = input("\nPress enter to continue")


def init_menus():
    response = send_command("help")
    entries = response.split('\n')
    entries = [e.split(' ') for e in entries]
    global MENU
    removed = ["login"]
    MENU = [(e[0], e[1:]) for e in entries if e[0] not in removed]


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
        if action in ["logout", "exit"]:
            return action
        print("Invalid input")
        input("\nPress enter to continue")
        return generate_command()
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
        response = send_command(f"login _ _ {username} {password}")
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
    global BREAK
    BUFF_SIZE = 65536
    BREAK = False
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    message = b'Hello'
    client_socket.sendto(message, (ADDRESS, video_port))

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(audio_stream, ADDRESS, audio_port)
        executor.submit(video_stream, client_socket, BUFF_SIZE)


def video_stream(client_socket, BUFF_SIZE):
    global BREAK
    cv2.namedWindow('RECEIVING VIDEO')
    cv2.moveWindow('RECEIVING VIDEO', 10, 360)
    cv2.startWindowThread()
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    while not BREAK:
        packet, _ = client_socket.recvfrom(BUFF_SIZE)
        if packet.decode() == "finished":
            break
        data = base64.b64decode(packet, ' /')
        npdata = np.frombuffer(data, dtype=np.uint8)

        frame = cv2.imdecode(npdata, 1)
        frame = cv2.putText(frame, 'FPS: '+str(fps), (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF

        #if key == ord('q'):
        #    client_socket.close()
            # os._exit(1)
        #    break

        

        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1
    print("Video Closed!")
    client_socket.close()
    cv2.destroyAllWindows()


def audio_stream(host_ip, port):
    global BREAK
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
    client_socket.connect(socket_address)
    data = b""
    payload_size = struct.calcsize("Q")
    while not BREAK:
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
    print('Audio closed!')


# use this after connecting to server socket!
def send_data(port: int, file_path: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDRESS, port))
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

def stop_playing():
    global BREAK
    BREAK = True

def set_proxy():
    global EN_PROXY
    EN_PROXY = input("Use proxy? (y/n): ") == "y"
    if EN_PROXY:
        global PROXY_ADDRESS
        PROXY_ADDRESS = input("Proxy address: ")
        global PROXY_USERNAME
        PROXY_USERNAME = input("Proxy username: ")
        global PROXY_PASSWORD
        PROXY_PASSWORD = input("Proxy password: ")
        print("Proxy settings set!")
    

if __name__ == '__main__':
    global BREAK
    BREAK = False
    keyboard.add_hotkey('q', lambda: stop_playing())
    if len(sys.argv) > 1:
        ADDRESS = sys.argv[1]
    set_proxy()
    init_menus()
    run()
