from extraction.models import *
from django.core.management.base import BaseCommand
from extraction.lib.praw_utils import create_praw_instace
import requests
from datetime import datetime, timezone

class Command(BaseCommand):
    help = "Extract historical data from authors, submissions and comments from subreddits"

    def add_arguments(self, parser):
        parser.add_argument("--limit_date", type=str, help="limit_date (default = today)")

    def handle(self, *args, **options):
        limit_date = options["limit_date"]
        reddit = create_praw_instace()

        payload = {
            "subreddit": "investimentos"
        }

        result = requests.get("https://api.pushshift.io/reddit/submission/search", params=payload)

        for i, submission in enumerate(result.json()["data"]):         
            author_praw = reddit.redditor(submission["author"])
            submission_praw = reddit.submission(submission["id"])    

            Author.objects.update_or_create(
                id = author_praw.id,
                username = author_praw.name,
                created_utc = datetime.fromtimestamp(author_praw.created_utc, tz=timezone.utc),
                defaults={
                    "has_verified_email": author_praw.has_verified_email,
                    "karma": author_praw.link_karma,
                    "extraction_date": datetime.now(tz=timezone.utc)
                }
            )

            Submission.objects.update_or_create(
                id = submission_praw.id,
                author = Author.objects.get(id=author_praw.id),
                subreddit = Subreddit.objects.get(id=submission["subreddit_id"]),
                created_utc = datetime.fromtimestamp(submission_praw.created_utc, tz=timezone.utc),
                defaults={
                    "name": submission_praw.name,
                    "title": submission_praw.title,
                    "selftext": submission_praw.selftext,
                    "distinguished": submission_praw.distinguished,
                    "spoiler": submission_praw.spoiler,
                    "allow_live_comments": submission["allow_live_comments"],
                    "is_video": submission["media_only"],
                    "media_only": submission["media_only"],
                    "is_self": submission_praw.is_self,
                    "is_original_content": submission_praw.is_original_content,
                    "link_flair_text": submission_praw.link_flair_text,
                    "num_comments": submission_praw.num_comments,
                    "over_18": submission_praw.over_18,
                    "permalink": submission_praw.permalink,
                    "score": submission_praw.score,
                    "url": submission_praw.url,
                    "edited": submission_praw.edited,
                    "upvote_ratio": submission_praw.upvote_ratio,
                    "extraction_date": datetime.now(tz=timezone.utc)
                }
            )

            for tag in submission["treatment_tags"]:
                TreatmentTags.objects.create(
                    title = tag,
                    submission = Submission.objects.get(id=submission["id"]),
                    subreddit = Subreddit.objects.get(id=submission["subreddit_id"])
                )

            for comment in submission_praw.comments:
                comment_praw = reddit.comment(comment.id)

                author_comment_praw = reddit.redditor(comment_praw.author)

                Author.objects.update_or_create(
                    id = author_comment_praw.id,
                    username = author_comment_praw.name,
                    created_utc = datetime.fromtimestamp(author_comment_praw.created_utc, tz=timezone.utc),
                    defaults={
                        "has_verified_email": author_comment_praw.has_verified_email,
                        "karma": author_comment_praw.link_karma,
                        "extraction_date": datetime.now(tz=timezone.utc)
                    }
                )

                Comment.objects.update_or_create(
                    id = comment_praw.id,
                    author = Author.objects.get(id=author_comment_praw.id),
                    subreddit = Subreddit.objects.get(id=submission["subreddit_id"]),
                    submission = Submission.objects.get(id=submission["id"]),
                    created_utc = datetime.fromtimestamp(comment_praw.created_utc, tz=timezone.utc),
                    defaults={
                        "parent_id": comment_praw.parent_id,
                        "body": comment_praw.body,
                        "distinguished": comment_praw.distinguished,
                        "is_submitter": comment_praw.is_submitter,
                        "score": comment_praw.score,
                        "permalink": comment_praw.permalink,
                        "extraction_date": datetime.now(tz=timezone.utc)
                    }  
                )

            #if i==999: print("Change dates")