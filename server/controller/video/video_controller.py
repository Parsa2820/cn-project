# TODO: Soheil
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

