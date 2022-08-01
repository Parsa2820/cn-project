from models.account.account import Account
from datahandler.datahandler import DataHandler


def login_ok(datahandler: DataHandler, username: str, password: str) -> bool:
    """
    Checks username and password.
    """
    try:
        account = datahandler.get_account_by_username(username)
    except KeyError:
        return False
    if account.password == password:
        return True
    return False


def login(datahandler: DataHandler, username: str, password: str) -> str:
    """
    Logs in the user.
    """
    if login_ok(datahandler, username, password):
        return "Login successful"
    return "Login failed"


def register_user(datahandler: DataHandler, username: str, password: str) -> str:
    """
    Registers the user.
    """
    try:
        account = datahandler.get_account_by_username(username)
        return "Username already exists"
    except KeyError:
        account = Account("user", username, password)
        datahandler.add_account(account)
        return "Registration successful"

# TODO: SARA