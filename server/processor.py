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
    # TODO: Add private functions here
}


def process(input: str) -> str:
    """
    Processes the command and returns the result.
    """
    datahandler = DataHandler("../data/")
    command, username, password, *args = input.lower().split()
    try:
        if (username, password) == ("_", "_"):
            return public_functions[command](datahandler, *args)
        else:
            if login_ok(datahandler, username, password):
                return private_functions[command](datahandler, username, *args)
            else:
                return "Login failed"
    except TypeError as e:
        return "Error: " + str(e)
