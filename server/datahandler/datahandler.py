from typing import List
import os
import json
from models.account.account import Account
# from models.ticket.ticket import Ticket
from models.video.video import Video


class DataHandler:
    ACCOUNTS_FILE = "accounts.json"
    VIDEOS_FILE = "videos.json"
    TICKET_FILE = "tickets.json"
    def __init__(self, data_directory: str) -> None:
        self.data_directory: str = data_directory
        self.__check_data_directory()

    def __check_data_directory(self) -> None:
        if not os.path.exists(self.data_directory):
            raise Exception("Data directory does not exist")
        if len(os.listdir(self.data_directory)) > 0:
            if not self.__exist_files():
                raise Exception("Data directory does not contain this application's data")
        else:
            self.__init_files()

    def __exist_files(self) -> bool:
        return os.path.exists(os.path.join(self.data_directory, self.ACCOUNTS_FILE)) and \
               os.path.exists(os.path.join(self.data_directory, self.VIDEOS_FILE)) and \
               os.path.exists(os.path.join(self.data_directory, self.TICKET_FILE))

    def __init_files(self) -> None:
        empty = []
        with open(os.path.join(self.data_directory, self.ACCOUNTS_FILE), "w") as f:
            json.dump(empty, f)
        with open(os.path.join(self.data_directory, self.VIDEOS_FILE), "w") as f:
            json.dump(empty, f)
        with open(os.path.join(self.data_directory, self.TICKET_FILE), "w") as f:
            json.dump(empty, f)
    
    def get_accounts(self) -> List[Account]:
        with open(os.path.join(self.data_directory, self.ACCOUNTS_FILE), "r") as f:
            accounts = json.load(f)
        return [Account.from_json(account) for account in accounts]

    def add_account(self, account: Account) -> None:
        accounts = self.get_accounts()
        accounts.append(account)
        with open(os.path.join(self.data_directory, self.ACCOUNTS_FILE), "w") as f:
            json.dump(accounts, f, default=lambda o: o.__dict__, indent=4)

    def get_videos(self) -> List[Video]:
        with open(os.path.join(self.data_directory, self.VIDEOS_FILE), "r") as f:
            pass



    
