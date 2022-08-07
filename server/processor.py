import inspect
from typing import Callable
import logging

from datahandler.datahandler import DataHandler
from controller.account.account_controller import *
from controller.support.ticket_controller import *
from controller.video.video_controller import *
from common.errors import PermissionError

public_functions = {
    "login": login,
    "register_user": register_user,
    "register_admin": register_admin,
    "get_available_videos": get_available_videos_public,
    "watch_video": watch_video
}

private_functions = {
    # Support related commands!
    "get_tickets": get_tickets,
    "create_ticket": create_ticket,
    "reply_ticket": reply_ticket,
    "new_ticket": new_ticket,
    "pend_ticket": pend_ticket,
    "resolve_ticket": resolve_ticket,
    "close_ticket": close_ticket,
    # Video related commands!
    "get_videos_by_username": get_videos_by_username,
    "get_banned_and_normal_videos": get_all_videos,
    "get_banned_videos": get_banned_videos,
    "like_video": like_video,
    "dislike_video": dislike_video,
    "unlike_video": unlike_video,
    "undislike_video": undislike_video,
    "comment_video": comment_video,
    "upload_video": upload_video,
    "ban_video": ban_video,
    "unban_video": unban_video,
    "add_tag": add_tag,
    # account related commands
    "unban_account": unban_account,  # admin
    "reject_admin_account": reject_admin_account,  # manager
    "accept_admin_account": accept_admin_account  # manager
    # TODO: Add private functions here
}


def generate_funtion_help(name: str, f: Callable) -> str:
    """
    Generates the help message for a funtion.
    """
    args = inspect.getfullargspec(f).args[1:]
    return f"{name} {' '.join(args)}"


def generate_help() -> str:
    """
    Generates the help message for the commands.
    """
    funtions_help = []
    for key, value in public_functions.items():
        funtions_help.append(generate_funtion_help(key, value))
    for key, value in private_functions.items():
        funtions_help.append(generate_funtion_help(key, value))
    return "\n".join(funtions_help)


def process(datahandler: DataHandler, input: str) -> str:
    """
    Processes the command and returns the result.
    """
    if input.startswith("help"):
        return generate_help()
    try:
        command, username, password, *args = input.lower().split()
        if (username, password) == ("_", "_"):
            return public_functions[command](datahandler, *args)
        else:
            if login_ok(datahandler, username, password):
                if command in public_functions.keys():
                    return public_functions[command](datahandler, *args)
                elif command in private_functions.keys():
                    return private_functions[command](datahandler, *args)
                else:
                    return "Command not found"
            else:
                return "Login failed"
    except (TypeError, KeyError, PermissionError) as e:
        logging.error(e)
        return "Error: " + str(e)
