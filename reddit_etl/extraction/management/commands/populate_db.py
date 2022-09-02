from distutils.command.build_scripts import first_line_re
from extraction.models import *
from django.core.management.base import BaseCommand
from extraction.lib.praw_utils import create_praw_instace
import requests
from datetime import datetime, timezone, timedelta
from tqdm import tqdm

class Command(BaseCommand):
    help = "Extract historical data from authors, submissions and comments from subreddits"

    def add_arguments(self, parser):
        parser.add_argument("--subreddit", default=None, type=str, help="Extraction for just one subreddit")
        parser.add_argument("--before", default=None, type=str, help="Extraction for all submissions before some date (yyyy-mm-dd)")
        parser.add_argument("--after", default=None, type=str, help="Extraction for all submissions after some date (yyyy-mm-dd)")

    def handle(self, *args, **options):
        before = options["before"]
        after = options["after"]
        reddit = create_praw_instace()
        first_after = None

        subreddit_list = [s.name for s in Subreddit.objects.all()]
        if not options["subreddit"] is None:
            if options["subreddit"] in subreddit_list:
                subreddit_list = [options["subreddit"]]
            else:
                subreddit_metadata = reddit.subreddit(options["subreddit"])     
                Subreddit.objects.update_or_create(
                    id = f"t5_{subreddit_metadata.id}",
                    name = subreddit_metadata.display_name,
                    created_utc = datetime.fromtimestamp(subreddit_metadata.created_utc, tz=timezone.utc),
                    defaults={
                        "description": subreddit_metadata.description,
                        "n_subscribers": subreddit_metadata.subscribers,
                        "over_18": subreddit_metadata.over18,
                        "extraction_date": datetime.now(tz=timezone.utc),
                    }
                )

            

        if before is None: 
            before = int((datetime.now(timezone.utc) + timedelta(hours=-6)).timestamp())
        else:
            before = int((datetime.fromisoformat(before)).timestamp())
          

        if after is None: 
            first_after = [int(s.created_utc.timestamp()) for s in Subreddit.objects.all() if s.name in subreddit_list]
        else: 
            first_after = int((datetime.fromisoformat(after)).timestamp())

        print(before)

        for subreddit_to_extract in subreddit_list:
            print(f"Extracting from r/{subreddit_to_extract}")

            if type(first_after) is list:
                after = first_after.pop(0)
            else: 
                after = first_after

            while int((datetime.utcfromtimestamp(after) + timedelta(hours=+6)).timestamp()) < before:
                print('before', datetime.utcfromtimestamp(before))
                print('after', datetime.utcfromtimestamp(after))

                payload = {
                    "subreddit": subreddit_to_extract.lower(),
                    "before": before,
                    "after": after,
                    "limit": 250,
                }

                result = requests.get("https://api.pushshift.io/reddit/submission/search", params=payload)

                for submission in result.json()["data"]:         
                    author_praw = reddit.redditor(submission["author"])
                    submission_praw = reddit.submission(submission["id"])    

                    try: 
                        author_removed = False
                        author_praw.id is None
                    except:
                        author_removed = True

                    if author_removed:
                        Author.objects.update_or_create(
                            id ='removed',
                            username = None,
                            created_utc = datetime(1970,1,1, tzinfo=timezone.utc),
                            defaults={
                                "has_verified_email": False,
                                "karma": 0,
                                "extraction_date": datetime.now(tz=timezone.utc)
                            }
                        )
                        author_id = 'removed'

                    else:
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
                        author_id = author_praw.id


                    Submission.objects.update_or_create(
                        id = submission_praw.id,
                        author = Author.objects.get(id=author_id),
                        subreddit = Subreddit.objects.get(id=submission["subreddit_id"]),
                        created_utc = datetime.fromtimestamp(submission_praw.created_utc, tz=timezone.utc),
                        defaults={
                            "name": submission_praw.name,
                            "title": submission_praw.title,
                            "selftext": submission_praw.selftext,
                            "distinguished": submission_praw.distinguished,
                            "spoiler": submission_praw.spoiler,
                            "allow_live_comments": submission["allow_live_comments"],
                            "is_video": submission["is_video"],
                            "media_only": submission["media_only"],
                            "is_self": submission_praw.is_self,
                            "is_original_content": submission_praw.is_original_content,
                            "link_flair_text": submission_praw.link_flair_text,
                            "num_comments": submission_praw.num_comments,
                            "over_18": submission_praw.over_18,
                            "permalink": submission_praw.permalink,
                            "score": submission_praw.score,
                            "url": submission_praw.url,
                            "edited": datetime.fromtimestamp(submission_praw.edited, tz=timezone.utc),
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
                        
                        if comment_praw.author is None:
                            author_removed = True
                        else:
                            author_removed = False

                        try:
                            author_comment_praw = reddit.redditor(comment_praw.author)
                            author_comment_praw.id
                        except:
                            author_removed = True
                      
                        if author_removed:
                            Author.objects.update_or_create(
                                id ='removed',
                                username = None,
                                created_utc = datetime(1970,1,1, tzinfo=timezone.utc),
                                defaults={
                                    "has_verified_email": False,
                                    "karma": 0,
                                    "extraction_date": datetime.now(tz=timezone.utc)
                                }
                            )   
                            author_id = 'removed'

                        else:
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
                            author_id = author_comment_praw.id

                        Comment.objects.update_or_create(
                            id = comment_praw.id,
                            author = Author.objects.get(id=author_id),
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

                after = int(submission_praw.created_utc)

            print(f"Finished extraction from r/{subreddit_to_extract}")  