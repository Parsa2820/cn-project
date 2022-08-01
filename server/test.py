from datahandler.datahandler import DataHandler
from models.account.account import Account
from models.support.ticket import Ticket, Reply
from models.video.video import Video


datahandler = DataHandler("./test_data")
account = Account("user", "majid", "user")
ticket = Ticket(1, account, "message")
ticket.replies.append(Reply(account, "message"))
ticket.replies.append(Reply(account, "message"))
datahandler.add_ticket(ticket)
print(datahandler.get_tickets())
print(str(datahandler.get_tickets()[0]))
print(datahandler.count_tickets())
ticket = datahandler.get_tickets()[0]
ticket.status = "closed"
datahandler.update_ticket(ticket)
print(datahandler.get_tickets()[0])

video = Video(datahandler.count_videos() , "test video" , " This is a test video ! ", "majid")
datahandler.add_video(video)
video.add_comment(datahandler.count_comments_of_video(video),"majid", "comment number one!")
datahandler.update_video(video)
video.add_comment(datahandler.count_comments_of_video(video),"majid", "comment number two!")
datahandler.update_video(video)
video2 = Video(datahandler.count_videos(), "test video 2", "this is another test video", "soheil")
datahandler.add_video(video2)
video2.ban_video()
datahandler.update_video(video2)
video2.unban_video()
video2.like_video("soheil")
video2.like_video("mamad")
video2.dislike_video("majid")
datahandler.update_video(video2)
videos = datahandler.get_videos()
for video in videos:
    print(str(video))
