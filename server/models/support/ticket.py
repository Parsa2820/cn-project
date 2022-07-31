from typing import List
from models.account.account import Account


class Reply:
    def __init__(self, account: Account, message: str):
        self.account: Account = account
        self.message: str = message

    def from_json(json_data: dict):
        return Reply(Account.from_json(json_data["account"]), json_data["message"])

    def __str__(self):
        return "{}: {}".format(str(self.account), self.message)


class Ticket:
    def __init__(self, id, account: Account, message: str):
        self.id = id
        self.account: Account = account
        self.message: str = message
        self.status = "new"
        self.replies: List[Reply] = []

    def from_json(json_data: dict):
        ticket = Ticket(Account.from_json(json_data["id"],
                                          json_data["account"]), json_data["message"])
        ticket.status = json_data["status"]
        ticket.replies = [Reply.from_json(reply)
                          for reply in json_data["replies"]]
        return ticket

    def __str__(self):
        return "Ticket {} from {}: {}".format(id, str(self.account), self.message) \
            + "\nStatus: {}".format(self.status) \
            + "\nReplies:\n\t" \
            + "\n\t".join([str(reply) for reply in self.replies])
