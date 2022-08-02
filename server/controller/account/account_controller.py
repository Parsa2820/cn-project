from models.account.account import Account
from models.account.request import Request
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

def register_admin(datahandler: DataHandler, username: str, password: str) -> str:
    """
    Registers the admin.
    """
    try:
        datahandler.get_account_by_username(username)
        return "Username already exists"
    except KeyError:
        request = Request(username, password)
        datahandler.add_request(request)
        return "request sent"

def accept_admin_account(datahandler: DataHandler, manager_username:str, username: str) -> str:
    """
    Accepts the account.
    """
    manager_account = datahandler.get_account_by_username(manager_username)
    if manager_account.account_type != "manager":
        raise PermissionError("You don't have the permission to accept user!")
    try:
        request = datahandler.get_request_by_id(username)
    except KeyError:
        return "Request does not exist"
    request.status = "accepted"
    datahandler.update_request(request)
    account = Account("admin", username, request.password)
    datahandler.add_account(account)
    return "Account accepted"

def reject_admin_account(datahandler: DataHandler, manager_username:str, username: str) -> str:
    """
    Rejects the account.
    """
    manager_account = datahandler.get_account_by_username(manager_username)
    if manager_account.account_type != "manager":
        raise PermissionError("You don't have the permission to reject user!")
    try:
        request = datahandler.get_request_by_id(username)
    except KeyError:
        return "Request does not exist"
    request.status = "rejected"
    datahandler.update_request(request)
    return "Account rejected"

def unban_account(datahandler: DataHandler, admin_username: str, username: str) -> str:
    """
    Unbans the account.
    """
    admin_account = datahandler.get_account_by_username(admin_username)
    if admin_account.account_type != "admin":
        raise PermissionError("You don't have the permission to unban user!")
    try:
        account = datahandler.get_account_by_username(username)
    except KeyError:
        return "Account does not exist"
    account.is_banned = False
    datahandler.update_account(account)
    return "Account unbanned"

# TODO: SARA