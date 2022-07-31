# TODO SOHEIL

from server.models.video.comment import Comment


class Video():
    """
    """
    video_counter: int = 0
    all_videos = list()

    def __init__(self, title: str, description: str, uploader_username: str):
        """
        Constructor of Video:
        is_new: bool variable indicating if the object is being creating or loaded from DB!
        title: title of video!
        description: description of video!
        uploader_username: username of the user who uploaded the video!
        is_available: boolean to show if the video is blocked or not!
        comment_counter: number of comments!
        comments: list of comments!
        video_id: unique identifier of the video generated according to the number of videos created till now!
        video_path: path that the video will be written to and read from!
        likes: list of the likers' usernames!
        dislikes: list of the dislikers' usernames!
        """
        self.title = title
        self.description = description
        self.uploader_username = uploader_username
        self.is_available = True
        self.comment_counter = 0
        self.comments = list()
        Video.video_counter += 1 #TODO need to read this from database!
        self.video_id = 0 # TODO need to increment video_counter!
        self.video_path = "./video_0" # TODO need to generate video_path!
        self.likes = set() # TODO
        self.dislikes = set() # TODO

        Video.all_videos.append(self)
    
    @classmethod
    def generate_video_id(cls) -> str:
        """
        class method to generate id for a video according to the number of videos till now!
        """
        output = f'{cls.video_counter}'
        return output

    @classmethod
    def set_video_counter(cls, value: int) -> None:
        """
        class method to set the value of static variable video_counter!
        hint: this method is probably used upon reading the data from database!
        """
        cls.video_counter = value

    @classmethod
    def add_video_from_database(cls, title: str, description: str, uploader_username: str, is_available: bool, 
    comments: list, video_id: str, video_path: str, likes: list, dislikes: list):
        """
        """
        # TODO

    def add_comment(self, username: str, text: str) -> None:
        """
        adds a comment to comments' list!
        requires username of the commenter and the text!
        """
        comment = Comment(self.generate_comment_id(), username, text)
        self.comment_counter += 1
        self.comments.append(comment)

    def generate_comment_id(self) -> str:
        """
        generates a comment id based on the current comment_counter!
        """
        output = f'{self.comment_counter}'
        return output

    def has_user_liked(self, username: str) -> bool:
        """
        checks if the username is in the likes set!
        """
        return username in self.likes

    def has_user_disliked(self, username: str) -> bool:
        """
        checks if the username is in the dislikes set!
        """
        return username in self.dislikes

    def like_video(self, username: str) -> None:
        """
        like the video!
        if already liked nothing happends!
        if disliked before, removed from dislikes set and added to likes set!
        """
        if self.has_user_liked:
            return
        elif self.has_user_disliked:
            self.dislikes.remove(username)
            self.likes.add(username)
            return
        else:
            self.likes.add(username)
    
    def dislike_video(self, username: str) -> None:
        """
        dislike the video!
        if already disliked nothing happends!
        if liked before, removed from likes set and added to dislikes set!
        """
        if self.has_user_disliked:
            return
        elif self.has_user_liked:
            self.likes.remove(username)
            self.dislikes.add(username)
            return
        else:
            self.dislikes.add(username)

    def unlike_video(self, username: str) -> None:
        """
        remove username from liked set!
        """
        self.likes.remove(username)
    
    def undislike_video(self, username: str) -> None:
        """
        remove username from disliked set!
        """
        self.dislikes.remove(username)
    
    def get_videos_by_username(self, username: str) -> list:
        """
        returns the list of videos uploaded by a user!
        """
        videos = list()
        for video in self.all_videos: # TODO
            if video.uploader_username == username:
                videos.append(video)
        return videos



    
    

