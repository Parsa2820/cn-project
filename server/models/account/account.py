from abc import ABC, abstractmethod
import re

class Account(ABC):

    all_accounts = []

    def __init__(self, values):
        self.username = values[0]
        self.password = values[1]
        self.online = False
        Account.all_accounts.append(self)


