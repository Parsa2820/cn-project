from gpg import Data
from datahandler.datahandler import DataHandler
from controller.account.account_controller import *
from controller.support.ticket_controller import *
from controller.video.video_controller import *

public_functions = {
    "login": login,
    "register": register_user,
    # TODO: Add public functions here
}

private_functions = {
    "get_tickets": get_tickets,
    "create_ticket": create_ticket,
    "reply_ticket": reply_ticket,
    "new_ticket": new_ticket,
    "pend_ticket": pend_ticket,
    "resolve_ticket": resolve_ticket,
    "close_ticket": close_ticket,
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
