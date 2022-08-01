# TODO SOHEIL

class Comment():
    """
    Comment class representing comments of videos!
    each comment has a id, username of the user who posted it and a text!
    """
    def __init__(self, comment_id: int, commenter_username: str, comment_text: str):
        """
        Constructor of Comment class!
        comment_id: identifier of a comment! (it unique when paired with video_id)
        commenter_username: username of the user who posted the comment!
        comment_text: content of the comment!
        """
        self.comment_id = comment_id
        self.commenter_username = commenter_username
        self.comment_text = comment_text

    def from_json(json: dict):
        comment = Comment(json['comment_id'], json['commenter_username'], json['comment_text'])
        return comment

    def __str__(self) -> str:
        return "User {} commented: {}" .format(self.commenter_username, self.comment_text)

