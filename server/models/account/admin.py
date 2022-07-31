from user import User

class Admin():

    def __init__(self, values):
         super().__init__(values)

    def add_admin(self, values):
        Admin(values)

    def strike(self, username):
        user = User.find_user(username)
        if user is None:
            return "username not found"
        else:
            user.strike = True
            return "user struck"

    def ban_video(self,viedo_name):
        pass

    def add_tag(self, tag_name, video_name):
        pass
