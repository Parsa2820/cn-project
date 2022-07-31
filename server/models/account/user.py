import re


class User:

    all_users = []

    # regex
    username_reg = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
    password_reg = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[#$^+=!*()@%&]).{8,10}$')


    def __init__(self, values):
        super().__init__(values)
        self.videos = []
        self.strike = False
        User.all_users.append(self)

    def check_user(value):
        ok = False
        if re.search(User.username_reg, value[0]) is None:
            msg = "username error"
        elif re.search(User.password_reg, value[6]) is None:
            msg = "password error"
        else:
            ok = True
        return msg, ok

    def change_pass(value, user):
        if re.search(User.password_reg, value) is None:
            msg = "password error"
        else:
            user.password = value
            msg = "password changed"
        return msg

    def find_user(username):
        for i in User.all_users:
            if i.username == username:
                return i
        return None

    def add_user(values):
        if User.find_user(values[0]) is not None:
            return "username already exists"
        msg, ok = User.check_user(values)
        if ok:
            User(values)
            msg = "user added"
        return msg

    def edit_user(username, value):
        user = User.find_user(username)
        if user is None:
            return "username not found"
        msg = User.change_user(value, user)
        return msg

    def delete_user(username):
        user = User.find_user(username)
        if user is None:
            msg = "username not found"
        else:
            User.all_users.remove(user)
            msg = "user deleted"
        return msg

    def login(username, password):
        user = User.find_user(username)
        if user is None:
            return "username not found"
        elif user.password != password:
            return "password not correct"
        else:
            user.online = True
            return "login"

    def logout(username, password):
        user = User.find_acc(username)
        if user is None:
            return "username not found"
        elif user.password != password:
            return "password not correct"
        else:
            user.online = False
            return "logout"


    def upload_video(video_name):
        pass

    def view_video(video_name):
        pass

    def comment(video_name, comment):
        pass

    def like(video_name):
        pass



