from datahandler.datahandler import DataHandler
from controller.account.account_controller import *
from controller.support.ticket_controller import *
from controller.video.video_controller import *

public_functions = {
    "login": login,
    "register": register_user,
    "get_available_videos": get_available_videos_public,
    "watch_video" : watch_video_public
    # TODO: Add public functions here
}

private_functions = {
    #Support related commands!
    "get_tickets": get_tickets,
    "create_ticket": create_ticket,
    "reply_ticket": reply_ticket,
    "new_ticket": new_ticket,
    "pend_ticket": pend_ticket,
    "resolve_ticket": resolve_ticket,
    "close_ticket": close_ticket,
    #Video related commands!
    "get_videos_by_username": get_videos_by_username,
    "get_all_videos": get_all_videos,
    "get_available_videos": get_available_videos,
    "get_banned_videos": get_banned_videos,
    "watch_video": watch_video,
    "like_video": like_video,
    "dislike_video": dislike_video,
    "unlike_video": unlike_video,
    "undislike_video": undislike_video,
    "comment_video": comment_video,
    "upload_video": upload_video,
    "ban_video": ban_video,
    "unban_video": unban_video,
    "add_tag" : add_tag
    # TODO: Add private functions here
}


def process(datahandler:DataHandler, input: str) -> str:
    """
    Processes the command and returns the result.
    """
    try:
        command, username, password, *args = input.lower().split()
        if (username, password) == ("_", "_"):
            return public_functions[command](datahandler, *args)
        else:
            if login_ok(datahandler, username, password):
                return private_functions[command](datahandler, *args)
            else:
                return "Login failed"
    except ValueError:
        return "Invalid command"
    except TypeError as e:
        return "Error: " + str(e)
    except KeyError as e:
        return "Error: " + str(e)
