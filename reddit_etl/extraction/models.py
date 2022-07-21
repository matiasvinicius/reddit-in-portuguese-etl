from pyexpat import model
from django.db import models
from django.utils import timezone

class Author(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    username = models.CharField(max_length=20)
    created_utc = models.DateTimeField()
    karma = models.IntegerField()
    has_verified_email = models.BooleanField()
    extraction_date = models.DateTimeField()

    def __str__(self):
        return self.username

class Subreddit(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=500)
    subscribers = models.IntegerField()
    created_utc = models.DateTimeField()
    over_18 = models.BooleanField()
    extraction_date = models.DateTimeField()


class Submission(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.SET_NULL)
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    selftext = models.TextField()
    created_utc = models.DateTimeField()
    distinguished = models.CharField(max_length=10)
    is_original_content = models.BooleanField()
    is_self = models.BooleanField()
    link_flair_text = models.CharField(max_length=10)
    num_comments = models.IntegerField()
    over_18 = models.BooleanField()
    permalink = models.CharField(max_length=255)
    score = models.IntegerField()
    url = models.CharField(max_length=300)
    edited = models.BooleanField()
    upvote_ratio = models.FloatField()