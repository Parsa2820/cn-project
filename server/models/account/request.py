class Request:
    def __init__(self, username: str, password: str):
        """
        status -> pending, accepted, rejected
        """
        self.username: str = username
        self.password: str = password
        self.status: str = "pending"

    def from_json(json_data: dict):
        return Request(json_data["status"], json_data["username"], json_data["password"])

    def __str__(self):
        return "{} {}".format(self.status, self.username)
