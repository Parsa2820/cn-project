from models.support.ticket import Ticket, Reply
from models.account.account import Account
from datahandler.datahandler import DataHandler
from common.errors import PermissionError


def get_tickets(datahandler: DataHandler, username: str) -> str:
    tickets = datahandler.get_tickets()
    account = datahandler.get_account_by_username(username)
    if account.account_type == "admin":
        return '\n'.join([str(t) for t in tickets if t.account.account_type == "user" or t.account.username == account.username])
    elif account.account_type == "manager":
        return '\n'.join([str(t) for t in tickets])
    else:
        return '\n'.join([str(t) for t in tickets if t.account.username == username])


def create_ticket(datahandler: DataHandler, username: str, message: str) -> str:
    account = datahandler.get_account_by_username(username)
    id = datahandler.count_tickets() + 1
    ticket = Ticket(id, account, message)
    datahandler.add_ticket(ticket)
    return str(ticket)


def reply_ticket(datahandler: DataHandler, username: str, ticket_id: int, message: str) -> str:
    ticket = datahandler.get_ticket_by_id(ticket_id)
    if ticket.status == "closed":
        raise PermissionError("Ticket is closed")
    account = datahandler.get_account_by_username(username)
    __check_ticket_permission(ticket, account)
    ticket.replies.append(Reply(account, message))
    ticket.to_pending()
    if account.account_type != "user":
        ticket.to_resolved()
    datahandler.update_ticket(ticket)
    return str(ticket)


def new_ticket(datahandler: DataHandler, username: str, ticket_id: int) -> str:
    ticket = datahandler.get_ticket_by_id(ticket_id)
    if ticket.status == "closed":
        raise PermissionError("Ticket is closed")
    account = datahandler.get_account_by_username(username)
    __check_ticket_permission(ticket, account)
    ticket.to_new()
    datahandler.update_ticket(ticket)
    return str(ticket)


def pend_ticket(datahandler: DataHandler, username: str, ticket_id: int) -> str:
    ticket = datahandler.get_ticket_by_id(ticket_id)
    if ticket.status == "closed":
        raise PermissionError("Ticket is closed")
    account = datahandler.get_account_by_username(username)
    __check_ticket_permission(ticket, account)
    ticket.to_pending()
    datahandler.update_ticket(ticket)
    return str(ticket)


def resolve_ticket(datahandler: DataHandler, username: str, ticket_id: int) -> str:
    ticket = datahandler.get_ticket_by_id(ticket_id)
    if ticket.status == "closed":
        raise PermissionError("Ticket is closed")
    account = datahandler.get_account_by_username(username)
    __check_ticket_permission(ticket, account)
    ticket.to_resolved()
    datahandler.update_ticket(ticket)
    return str(ticket)


def close_ticket(datahandler: DataHandler, username: str, ticket_id: int) -> str:
    ticket = datahandler.get_ticket_by_id(ticket_id)
    account = datahandler.get_account_by_username(username)
    __check_ticket_permission(ticket, account)
    ticket.to_closed()
    datahandler.update_ticket(ticket)
    return str(ticket)


def __check_ticket_permission(ticket: Ticket, account: Account) -> None:
    print(ticket.account.username, account.username)
    if account.account_type == "manager":
        if ticket.account.account_type == "user":
            raise PermissionError("only admins can change user tickets")
        else:
            return
    elif account.account_type == "user":
        if ticket.account.username != account.username:
            raise PermissionError("You can only modify your own tickets")
        else:
            return
    elif account.account_type == "admin":
        if ticket.account.username != account.username and ticket.account.account_type != "user":
            raise PermissionError(
                "You can only modify your own and user tickets")
        else:
            return
