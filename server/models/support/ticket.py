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
        ticket = Ticket(json_data["id"], Account.from_json(
            json_data["account"]), json_data["message"])
        ticket.status = json_data["status"]
        ticket.replies = [Reply.from_json(reply)
                          for reply in json_data["replies"]]
        return ticket

    def to_new(self):
        self.status = "new"

    def to_pending(self):
        self.status = "pending"

    def to_resolved(self):
        self.status = "resolved"

    def to_closed(self):
        self.status = "closed"

    def add_reply(self, reply: Reply):
        self.replies.append(reply)

    def __str__(self):
        return "Ticket {} from {}: {}".format(self.id, str(self.account), self.message) \
            + "\nStatus: {}".format(self.status) \
            + "\nReplies:\n\t" \
            + "\n\t".join([str(reply) for reply in self.replies])
