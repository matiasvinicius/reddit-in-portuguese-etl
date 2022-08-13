import praw
from decouple import config

def create_praw_instace():
    username = config("REDDITUSER")
    reddit = praw.Reddit(
        client_id=config("REDDITID"),
        client_secret=config("REDDITKEY"),
        user_agent=username,
        username=f"research_pt by u/{username}"
    )
    return reddit