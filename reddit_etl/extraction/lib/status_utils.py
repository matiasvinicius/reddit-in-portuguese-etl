from re import sub
from extraction import models

def get_last_submissions(n):
    last_submissions = models.Submission.objects.order_by('-extraction_date')[:10]
    for i, submission in enumerate(last_submissions):
        last_submissions[i].author_name = submission.author.username
        last_submissions[i].subreddit_name = submission.subreddit.name
    return last_submissions
