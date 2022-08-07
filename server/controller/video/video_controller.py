# TODO: Soheil
import cv2, imutils, socket
import time
import base64
import wave, pyaudio , pickle, struct
import queue
import os

from datahandler.datahandler import DataHandler
from models.video.video import Video
from controller.account.account_controller import unban_account

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
    return '\n'.join ([str(video) for video in videos if not video.is_available])

def upload_video(datahandler: DataHandler, username: str, title: str, description: str) -> str:
    account = datahandler.get_account_by_username(username)
    if account.account_type != "user":
        raise PermissionError("You don't have the permission to upload video!")
    if account.is_banned:
        raise PermissionError("You are banned!")
    # TODO: actually uploading the video!
    video_id = datahandler.count_videos()
    new_video = Video(video_id, title, description, username)
    datahandler.add_video(new_video)
    return str(new_video)

def create_video(datahandler: DataHandler, username: str):
    pass

# use this after accepting client socket!
def __receive_file(server_socket, video: Video) -> None:
    #serverSocket.connect()
    with open(video.video_path, 'wb') as f:
        print('file incoming...')
        while True:
            print('receiving data...')
            data = server_socket.recv(1024)
            if not data:
                break
            f.write(data)
    print(video.video_path + " has been Received!")
    server_socket.close()

def comment_video(datahandler: DataHandler, username: str, video_id: int, text: str) -> str:
    account = datahandler.get_account_by_username(username)
    video = datahandler.get_video_by_id(int(video_id))
    video.add_comment(datahandler.count_comments_of_video(video), account.username, text)
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

def ban_video(datahandler: DataHandler, username: str, video_id:int) -> str:
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

def watch_video_public(datahandler: DataHandler, video_id:int ) -> str:
    video = datahandler.get_video_by_id(int(video_id))
    if not video.is_available:
        raise PermissionError("This video is banned!")
    # TODO : actually stream the video!
    return str(video)

def watch_video(datahandler: DataHandler, username: str, video_id:int ) -> str:
    account = datahandler.get_account_by_username(username)
    video = datahandler.get_video_by_id(int(video_id))
    if (account.account_type == "user" or account.account_type == "public") and not video.is_available:
        raise PermissionError("This video is banned!")
    # TODO : actually stream the video!
    return str(video)

def __start_streaming(vid: Video):
    q = queue.Queue(maxsize=10)

    filename =  vid.video_path
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(filename,'temp.wav')
    os.system(command)

    BUFF_SIZE = 65536
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip =  socket.gethostbyname(host_name)
    print(host_ip)
    port = 9688
    socket_address = (host_ip,port)
    server_socket.bind(socket_address)
    print('Listening at:',socket_address)

    path = os.getcwd()
    vid = cv2.VideoCapture(path + '\\server\\video_0.mp4')
    FPS = vid.get(cv2.CAP_PROP_FPS)
    global TS
    TS = (0.5/FPS)
    BREAK=False
    print('FPS:',FPS,TS)
    totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    durationInSeconds = float(totalNoFrames) / float(FPS)
    d=vid.get(cv2.CAP_PROP_POS_MSEC)
    print(durationInSeconds,d)

    # starting the threads
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(__audio_stream, host_ip, port)
        executor.submit(__video_stream_gen, vid, q)
        executor.submit(__video_stream, server_socket, BUFF_SIZE, q, FPS)


def __video_stream_gen(vid, q: queue):
    WIDTH=400
    while(vid.isOpened()):
        try:
            _,frame = vid.read()
            frame = imutils.resize(frame,width=WIDTH)
            q.put(frame)
        except:
            os._exit(1)
    print('Player closed')
    BREAK=True
    vid.release()

def __video_stream(server_socket, BUFF_SIZE, q, FPS):
    global TS
    fps,st,frames_to_count,cnt = (0,0,1,0)
    cv2.namedWindow('TRANSMITTING VIDEO')        
    cv2.moveWindow('TRANSMITTING VIDEO', 10,30) 
    while True:
        msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ',client_addr)
        WIDTH=400
        
        while(True):
            frame = q.get()
            encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            server_socket.sendto(message,client_addr)
            frame = cv2.putText(frame,'FPS: '+str(round(fps,1)),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                    if fps>FPS:
                        TS+=0.001
                    elif fps<FPS:
                        TS-=0.001
                    else:
                        pass
                except:
                    pass
            cnt+=1
            
            
            
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(int(1000*TS)) & 0xFF	
            if key == ord('q'):
                os._exit(1)
                TS=False
                break	

def __audio_stream(host_ip, port):
    s = socket.socket()

    s.bind((host_ip, (port-1)))

    s.listen(5)
    CHUNK = 1024
    path = os.getcwd()
    wf = wave.open(path + '\\server\\temp.wav', 'rb')
    p = pyaudio.PyAudio()
    print('server listening at',(host_ip, (port-1)))
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    client_socket,addr = s.accept()

    while True:
        if client_socket:
            while True:
                data = wf.readframes(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
