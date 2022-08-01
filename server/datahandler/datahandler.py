from typing import List
import os
import json
from models.account.account import Account
from models.support.ticket import Ticket
from models.video.video import Video


class DataHandler:
    ACCOUNTS_FILE = "accounts.json"
    VIDEOS_FILE = "videos.json"
    TICKET_FILE = "tickets.json"
    DEFUALTS = [
        Account("public", "_", "_"),
        # Account("manager", "manager", "supreme_manager#2022")
        Account("manager", "manager", "123")
    ]

    def __init__(self, data_directory: str) -> None:
        self.data_directory: str = data_directory
        self.__check_data_directory()

    def __check_data_directory(self) -> None:
        if not os.path.exists(self.data_directory):
            raise Exception("Data directory does not exist")
        if len(os.listdir(self.data_directory)) > 0:
            if not self.__exist_files():
                raise Exception(
                    "Data directory does not contain this application's data")
        else:
            self.__init_files()

    def __exist_files(self) -> bool:
        return os.path.exists(os.path.join(self.data_directory, self.ACCOUNTS_FILE)) and \
            os.path.exists(os.path.join(self.data_directory, self.VIDEOS_FILE)) and \
            os.path.exists(os.path.join(self.data_directory, self.TICKET_FILE))

    def __init_files(self) -> None:
        empty = []
        with open(os.path.join(self.data_directory, self.ACCOUNTS_FILE), "w") as f:
            json.dump(DataHandler.DEFUALTS, f, default=lambda o: o.__dict__, indent=4)
        with open(os.path.join(self.data_directory, self.VIDEOS_FILE), "w") as f:
            json.dump(empty, f)
        with open(os.path.join(self.data_directory, self.TICKET_FILE), "w") as f:
            json.dump(empty, f)

    def get_accounts(self) -> List[Account]:
        with open(os.path.join(self.data_directory, self.ACCOUNTS_FILE), "r") as f:
            accounts = json.load(f)
        return [Account.from_json(account) for account in accounts]

    def get_account_by_username(self, username: str) -> Account:
        accounts = self.get_accounts()
        for account in accounts:
            if account.username == username:
                return account
        return None

    def count_accounts(self) -> int:
        return len(self.get_accounts())

    def add_account(self, account: Account) -> None:
        accounts = self.get_accounts()
        accounts.append(account)
        with open(os.path.join(self.data_directory, self.ACCOUNTS_FILE), "w") as f:
            json.dump(accounts, f, default=lambda o: o.__dict__, indent=4)

    def __remove_account(self, username: str):
        accounts = self.get_accounts()
        accounts = [
            account for account in accounts if account.username != username]
        with open(os.path.join(self.data_directory, self.ACCOUNTS_FILE), "w") as f:
            json.dump(accounts, f, default=lambda o: o.__dict__, indent=4)

    def update_account(self, account: Account) -> None:
        self.__remove_account(account.username)
        self.add_account(account)

    def get_videos(self) -> List[Video]:
        with open(os.path.join(self.data_directory, self.VIDEOS_FILE), "r") as f:
            videos = json.load(f)
        return [Video.from_json(video) for video in videos]

    def get_video_by_id():
        pass
        # TODO: Soheil

    def count_videos(self) -> int:
        return len(self.get_videos())

    def add_video(self, video: Video) -> None:
        videos = self.get_videos()
        videos.append(video)
        with open(os.path.join(self.data_directory, self.VIDEOS_FILE), "w") as f:
            json.dump(videos, f, default=lambda o: o.__dict__, indent=4)

    def __remove_video(self, id: int) -> None:
        videos = self.get_videos()
        videos = [video for video in videos if video.video_id != id]
        with open(os.path.join(self.data_directory, self.VIDEOS_FILE), "w") as f:
            json.dump(videos, f, default=lambda o: o.__dict__, indent=4)

    def update_video(self, video: Video) -> None:
        self.__remove_video(video.video_id)
        self.add_video(video)

    def count_comments_of_video(self, video: Video) -> int:
        # TODO: Soheil: use get_video_by_id()
        videos = self.get_videos()
        for single_video in videos:
            if single_video.video_id == video.video_id:
                return len(single_video.comments)
        return 0  # this should never happen!

    def get_tickets(self) -> List[Ticket]:
        with open(os.path.join(self.data_directory, self.TICKET_FILE), "r") as f:
            tickets = json.load(f)
        return [Ticket.from_json(ticket) for ticket in tickets]

    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        tickets = self.get_tickets()
        for ticket in tickets:
            if ticket.id == ticket_id:
                return ticket
        return None

    def count_tickets(self) -> int:
        return len(self.get_tickets())

    def add_ticket(self, ticket: Ticket) -> None:
        tickets = self.get_tickets()
        tickets.append(ticket)
        with open(os.path.join(self.data_directory, self.TICKET_FILE), "w") as f:
            json.dump(tickets, f, default=lambda o: o.__dict__, indent=4)

    def __remove_ticket(self, id: int):
        tickets = self.get_tickets()
        tickets = [ticket for ticket in tickets if ticket.id != id]
        with open(os.path.join(self.data_directory, self.TICKET_FILE), "w") as f:
            json.dump(tickets, f, default=lambda o: o.__dict__, indent=4)

    def update_ticket(self, ticket: Ticket) -> None:
        self.__remove_ticket(ticket.id)
        self.add_ticket(ticket)
