def process(input: str) -> str:
    """
    Processes the command and returns the result.
    """
    command, *args = input.split()
    try:
        if command == "login":
            return login(*args)
    except TypeError as e:
        return "Error: " + str(e)

def login(username: str, password: str) -> str:
    """
    Logs in the user.
    """
    return "Login successful."
        