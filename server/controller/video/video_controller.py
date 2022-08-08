from concurrent.futures import thread
from http import server
import cv2
import imutils
import socket
import time
import base64
import wave
import pyaudio
import pickle
import struct
import queue
import os
import threading
import logging

from datahandler.datahandler import DataHandler
from models.video.video import Video
from controller.account.account_controller import unban_account
from common.errors import PermissionError


def get_all_videos(datahandler: DataHandler, username: str) -> str:
    # TODO: user type check!
    account = datahandler.get_account_by_username(username)
    if account.account_type == "user":
        raise PermissionError("You can only see available videos!")
    videos = datahandler.get_videos()
    return '\n'.join([str(video) for video in videos])


def get_videos_by_username(datahandler: DataHandler, username: str) -> str:
    videos = datahandler.get_videos()
    account = datahandler.get_account_by_username(username)
    return '\n'.join([str(video) for video in videos if video.uploader_username == account.username])


def get_available_videos_public(datahandler: DataHandler) -> str:
    videos = datahandler.get_videos()
    return '\n'.join([str(video) for video in videos if video.is_available])


def get_available_videos(datahandler: DataHandler, username: str) -> str:
    videos = datahandler.get_videos()
    account = datahandler.get_account_by_username(username)
    return '\n'.join([str(video) for video in videos if video.is_available])


def get_banned_videos(datahandler: DataHandler, username: str) -> str:
    # TODO: user type check!
    account = datahandler.get_account_by_username(username)
    if account.account_type == "user":
        raise PermissionError("You can only see available videos!")
    videos = datahandler.get_videos()
    return '\n'.join([str(video) for video in videos if not video.is_available])


def upload_video(datahandler: DataHandler, username: str, title: str, description: str) -> str:
    account = datahandler.get_account_by_username(username)
    if account.account_type != "user":
        raise PermissionError("You don't have the permission to upload video!")
    if account.is_banned:
        raise PermissionError("You are banned!")
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    video_id = datahandler.count_videos()
    new_video = Video(video_id, title, description, username)
    datahandler.add_video(new_video)
    threading.Thread(target=__receive_file, args=(s, new_video)).start()
    return str(port)


def __receive_file(server_socket: socket.socket, video: Video) -> None:
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    # TODO: check address later
    with open(video.video_path, 'wb') as f:
        logging.info(f'file {video.video_id} incoming...')
        while True:
            logging.debug(f'receiving {video.video_id} data...')
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
    logging.info(f'file {video.video_id} has been Received!')
    filename = video.video_path
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(
        filename, f'{filename}.wav')
    os.system(command)
    server_socket.close()


def comment_video(datahandler: DataHandler, username: str, video_id: int, text: str) -> str:
    account = datahandler.get_account_by_username(username)
    video = datahandler.get_video_by_id(int(video_id))
    video.add_comment(datahandler.count_comments_of_video(
        video), account.username, text)
    datahandler.update_video(video)
    return str(video)


def like_video(datahandler: DataHandler, username: str, video_id: int) -> str:
    account = datahandler.get_account_by_username(username)
    video = datahandler.get_video_by_id(int(video_id))
    video.like_video(account.username)
    datahandler.update_video(video)
    return str(video)


def dislike_video(datahandler: DataHandler, username: str, video_id: int) -> str:
    account = datahandler.get_account_by_username(username)
    video = datahandler.get_video_by_id(int(video_id))
    video.dislike_video(account.username)
    datahandler.update_video(video)
    return str(video)


def unlike_video(datahandler: DataHandler, username: str, video_id: int) -> str:
    account = datahandler.get_account_by_username(username)
    video = datahandler.get_video_by_id(int(video_id))
    video.unlike_video(account.username)
    datahandler.update_video(video)
    return str(video)


def undislike_video(datahandler: DataHandler, username: str, video_id: int) -> str:
    account = datahandler.get_account_by_username(username)
    video = datahandler.get_video_by_id(int(video_id))
    video.undislike_video(account.username)
    datahandler.update_video(video)
    return str(video)


def add_tag(datahandler: DataHandler, username: str, video_id: int, tag: str) -> str:
    # TODO: check user type!
    account = datahandler.get_account_by_username(username)
    if account.account_type == "user":
        raise PermissionError("You don't have the permission to add tags!")
    video = datahandler.get_video_by_id(int(video_id))
    video.add_tag(tag)
    datahandler.update_video(video)
    return str(video)


def ban_video(datahandler: DataHandler, username: str, video_id: int) -> str:
    # TODO: check user type!
    account = datahandler.get_account_by_username(username)
    if account.account_type == "user":
        raise PermissionError("You don't have the permission to ban videos!")
    video = datahandler.get_video_by_id(int(video_id))
    check_ban_user(datahandler, video.uploader_username)
    video.ban_video()
    datahandler.update_video(video)
    return str(video)


def get_banned_videos_username(datahandler: DataHandler) -> str:
    videos = datahandler.get_videos()
    return [video.uploader_username for video in videos if not video.is_available]


def check_ban_user(datahandler: DataHandler, username: str):
    account = datahandler.get_account_by_username(username)
    banned_videos_username = get_banned_videos_username(datahandler)
    for video_user in banned_videos_username:
        if video_user == username:
            account.is_banned = True
            datahandler.update_account(account)
            return


def unban_video(datahandler: DataHandler, username: str, video_id: int) -> str:
    # TODO: check user type!
    account = datahandler.get_account_by_username(username)
    if account.account_type == "user":
        raise PermissionError("You don't have the permission to unban videos!")
    video = datahandler.get_video_by_id(int(video_id))
    video.unban_video()
    datahandler.update_video(video)
    return str(video)


def watch_video(datahandler: DataHandler, video_id: int) -> str:
    video = datahandler.get_video_by_id(int(video_id))
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    video_socket.bind(('', 0))
    video_port = video_socket.getsockname()[1]
    audio_socket = socket.socket()
    audio_socket.bind(('', 0))
    audio_port = audio_socket.getsockname()[1]
    threading.Thread(target=__start_streaming, args=(
        video_socket, audio_socket, video)).start()
    return f"{video_port} {audio_port}"


def __start_streaming(video_socket: socket.socket, audio_socket: socket.socket, video: Video):
    global BREAK
    q = queue.Queue(maxsize=10)
    filename = video.video_path
    #command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(
    #    filename, f'{filename}.wav')
    #if(not os.path.exists(filename + '.wav')):  
    #    os.system(command)
    path = os.getcwd()
    vid = cv2.VideoCapture(path + '/' + filename)
    print(path + '/' + filename)
    FPS = vid.get(cv2.CAP_PROP_FPS)
    global TS
    TS = (0.5/FPS)
    BREAK = False
    print('FPS:', FPS, TS)
    totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    durationInSeconds = float(totalNoFrames) / float(FPS)
    d = vid.get(cv2.CAP_PROP_POS_MSEC)
    print(durationInSeconds, d)

    # starting the threads
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(__audio_stream, audio_socket, video)
        executor.submit(__video_stream_gen, vid, q)
        executor.submit(__video_stream, video_socket, 65536, q, FPS)


def __video_stream_gen(vid, q: queue):
    global BREAK
    WIDTH = 400
    while(vid.isOpened()):
        try:
            _, frame = vid.read()
            frame = imutils.resize(frame, width=WIDTH)
            q.put(frame)
        except:
            break
            #os._exit(1)
    print('Player closed')
    BREAK = True
    vid.release()


def __video_stream(server_socket, BUFF_SIZE, q, FPS):
    global TS, BREAK
    fps, st, frames_to_count, cnt = (0, 0, 1, 0)
    #cv2.namedWindow('TRANSMITTING VIDEO')
    #cv2.moveWindow('TRANSMITTING VIDEO', 10, 30)
    while True:
        #print("IM HERE")
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ', client_addr)
        WIDTH = 400

        while(True):
            if BREAK:
                server_socket.sendto("finished".encode(), client_addr)
                server_socket.close()
                print("socket closed!")
                return
            #print("IM HERE")
            frame = q.get()
            encoded, buffer = cv2.imencode(
                '.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            server_socket.sendto(message, client_addr)
            #frame = cv2.putText(frame, 'FPS: '+str(round(fps, 1)),
            #                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count/(time.time()-st))
                    st = time.time()
                    cnt = 0
                    if fps > FPS:
                        TS += 0.001
                    elif fps < FPS:
                        TS -= 0.001
                    else:
                        pass
                except:
                    pass
            cnt += 1

            #cv2.imshow('TRANSMITTING VIDEO', frame)
            #time.sleep(int(1000 * TS))
            #print("IM HERE")
            cv2.waitKey(int(1000*TS))
            #print("IM HERE")
            #if key == ord('q'):
                #os._exit(1)
            #    TS = False
            #    break


def __audio_stream(audio_socket: socket.socket, video: Video):

    audio_socket.listen(1)
    CHUNK = 1024
    path = os.getcwd()
    wf = wave.open(path + '/' + video.video_path + ".wav", 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    client_socket, addr = audio_socket.accept()

    for _ in range(0, wf.getnframes()//CHUNK):
        data = wf.readframes(CHUNK)
        a = pickle.dumps(data)
        message = struct.pack("Q", len(a))+a
        client_socket.sendall(message)
