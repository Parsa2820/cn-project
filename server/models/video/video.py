# TODO SOHEIL

from models.video.comment import Comment


class Video():
    """
    """
    def __init__(self, video_id: int, title: str, description: str, uploader_username: str):
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
        self.video_id = video_id
        self.video_path = self.__generate_video_path()
        self.description = description
        self.uploader_username = uploader_username
        self.is_available = True
        self.tags = list()
        self.comments = list()
        self.likes = list()
        self.dislikes = list() 
    
    def __generate_video_path(self):
        return f'./{self.title}_{self.video_id}.dat'

    def add_comment(self, comment_id: int, username: str, text: str) -> None:
        """
        adds a comment to comments' list!
        requires username of the commenter and the text!
        """
        comment = Comment(comment_id, username, text)
        self.comments.append(comment)

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
        if self.has_user_liked(username):
            return
        elif self.has_user_disliked(username):
            self.dislikes.remove(username)
            self.likes.append(username)
            return
        else:
            self.likes.append(username)
    
    def dislike_video(self, username: str) -> None:
        """
        dislike the video!
        if already disliked nothing happends!
        if liked before, removed from likes set and added to dislikes set!
        """
        if self.has_user_disliked(username):
            return
        elif self.has_user_liked(username):
            self.likes.remove(username)
            self.dislikes.append(username)
            return
        else:
            self.dislikes.append(username)

    def unlike_video(self, username: str) -> None:
        """
        remove username from liked set!
        """
        if username in self.likes:
            self.likes.remove(username)
    
    def undislike_video(self, username: str) -> None:
        """
        remove username from disliked set!
        """
        if username in self.dislikes:
            self.dislikes.remove(username)
    
    def get_videos_by_username(self, username: str) -> list:
        """
        returns the list of videos uploaded by a user!
        """
        pass

    def ban_video(self) -> None:
        """
        Makes the video unavailable!
        """
        self.is_available = False

    def unban_video(self) -> None:
        """
        Makes the video available!
        """
        self.is_available = True

    def count_likes(self) -> int:
        """
        returns the number of likes on this video!
        """
        return len(self.likes)

    def count_dislikes(self) -> int:
        """
        returns the number of dislikes on this video!
        """
        return len(self.dislikes)
    
    def add_tag(self, tag: str) -> None:
        """
        adds a tag to video!
        """
        self.tags.append(tag)

    def from_json(json: dict):
        video = Video(json['video_id'],json['title'],json['description']
                    ,json['uploader_username'])
        video.is_available = json['is_available']
        video.comments = [Comment.from_json(comment) for comment in json['comments']]
        video.video_path = json['video_path']
        video.tags = json['tags']
        video.likes = json['likes']
        video.dislikes = json['dislikes']
        return video


    def __str__(self) -> str:
        return "id: {} \n" .format(self.video_id) \
            + "Is available: {} \n" .format(self.is_available) \
            + "tags: \n\t" \
            + "\n\t" .join([tag for tag in self.tags]) \
            + "\ntitle: {} \n" .format(self.title) \
            + "description: {} \n" .format(self.description) \
            + "Likes: {} \n" .format(str(self.count_likes())) \
            + "DisLikes: {} \n" .format(str(self.count_dislikes())) \
            + "Comments: \n\t" \
            + "\n\t" .join([str(comment) for comment in self.comments])




        
    




    
    

