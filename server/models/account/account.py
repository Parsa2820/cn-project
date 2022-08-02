class Account:
    def __init__(self, account_type: str, username: str, password: str):
        """
        account_type -> user, manager, admin
        """
        self.account_type: str = account_type
        self.username: str = username
        self.password: str = password
        self.is_banned: bool = False

    def from_json(json_data: dict):
        account = Account(json_data["account_type"], json_data["username"], json_data["password"])
        account.is_banned = json_data["is_banned"]
        return account

    def __str__(self):
        return "{} {}".format(self.account_type, self.username)
