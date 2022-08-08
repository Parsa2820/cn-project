from models.account.account import Account
from models.account.request import Request
from datahandler.datahandler import DataHandler
from common.errors import PermissionError


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
        if(datahandler.get_request_by_id(username) or datahandler.get_account_by_username(username)):
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


def accept_admin_account(datahandler: DataHandler, username: str, admin_username: str) -> str:
    """
    Accepts the account.
    """
    manager_account = datahandler.get_account_by_username(username)
    if manager_account.account_type != "manager":
        raise PermissionError("You don't have the permission to accept user!")
    try:
        request = datahandler.get_request_by_id(admin_username)
    except KeyError:
        return "Request does not exist"
    request.status = "accepted"
    datahandler.update_request(request)
    account = Account("admin", admin_username, request.password)
    datahandler.add_account(account)
    return "Account accepted"


def reject_admin_account(datahandler: DataHandler, username: str, admin_username: str) -> str:
    """
    Rejects the account.
    """
    manager_account = datahandler.get_account_by_username(username)
    if manager_account.account_type != "manager":
        raise PermissionError("You don't have the permission to reject user!")
    try:
        request = datahandler.get_request_by_id(admin_username)
    except KeyError:
        return "Request does not exist"
    request.status = "rejected"
    datahandler.update_request(request)
    return "Account rejected"


def unban_account(datahandler: DataHandler, username: str, user_username: str) -> str:
    """
    Unbans the account.
    """
    admin_account = datahandler.get_account_by_username(username)
    if admin_account.account_type != "admin":
        raise PermissionError("You don't have the permission to unban user!")
    try:
        account = datahandler.get_account_by_username(user_username)
    except KeyError:
        return "Account does not exist"
    account.is_banned = False
    datahandler.update_account(account)
    return "Account unbanned"


def get_requests(datahandler: DataHandler, username: str) -> str:
    """
    Gets the requests.
    """
    user = datahandler.get_account_by_username(username)
    if user.account_type != "manager":
        raise PermissionError("You don't have the permission to get requests!")
    requests = datahandler.get_requests()
    return '\n'.join(str(request) for request in requests)
