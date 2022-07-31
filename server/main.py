from models.account.account import Account
from models.account.user import User
from models.account.manager import Manager
from models.account.admin import Admin

def add_manager():
    Manager.add_manager("manager", "2022#manager_s")

def CommandProcessor():
    inp = input("Enter command: ").lower().split(" ")

    def add_user():
        User.add_user(inp[1:2])

    def edit_user():
        User.edit_user(inp[1], inp[2])

    def delete_user():
        User.delete_user(inp[1])

    def upload_video():
        User.upload_video(inp[1])

    def view_video():
        User.view_video(inp[1])

    def comment():
        User.comment(inp[1], inp[2])
    
    def like():
        User.like(inp[1])

    def strike():
        Admin.strike(inp[1])

    def ban_video():
        Admin.ban_video(inp[1])

    def add_tag():
        Admin.add_tag(inp[1], inp[2])

    def login():
        User.login(inp[1], inp[2])

    def logout():
        User.logout(inp[1], inp[2])

    def help():
        help = [
            #account
            "login: login [username, password]",
            "logout: logout [username, password]",
            #
            "add user: adduser [username, password]",
            "edit user: edituser [username, value]",
            "delete user: deleteuser [username]",
            #user
            "upload video: uploadvideo [video_name]",
            "view video: viewvideo [video_name]",
            "comment: comment [video_name, comment]",
            "like: like [video_name]",
            #admin
            "strike: strike [username]",
            "ban video: banvideo [video_name]",
            "add tag: addtag [tag_name, video_name]",

            # helpers
            "help: help",
            "exit: exit"

        ]
        for i in help:
            print(i)

    def exit():
        pass

    def default():
        print("Invalid command")

    switcher = {
        "adduser": add_user,
        "edituser": edit_user,
        "deleteuser": delete_user,

        "uploadvideo": upload_video,
        "viewvideo": view_video,
        "comment": comment,
        "like": like,

        "strike": strike,
        "banvideo": ban_video,
        "addtag": add_tag,

        "login" : login,
        "logout": logout,

        "help": help,
        "exit": exit
    }

    return switcher.get(inp[0], lambda: default())()

if __name__ == '__main__':

    while True:
        CommandProcessor()