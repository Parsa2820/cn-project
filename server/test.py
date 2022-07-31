from datahandler.datahandler import DataHandler
from models.account.account import Account
from models.support.ticket import Ticket, Reply


datahandler = DataHandler("../test_data")
account = Account("user", "majid", "user")
ticket = Ticket(1, account, "message")
ticket.replies.append(Reply(account, "message"))
ticket.replies.append(Reply(account, "message"))
datahandler.add_ticket(ticket)
print(datahandler.get_tickets())
print(str(datahandler.get_tickets()[0]))
print(datahandler.count_tickets())
ticket = datahandler.get_tickets()[0]
ticket.status = "closed"
datahandler.update_ticket(ticket)
print(datahandler.get_tickets()[0])