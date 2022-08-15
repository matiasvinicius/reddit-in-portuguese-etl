from pyexpat import model
from django.db import models

class Author(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    username = models.CharField(max_length=20)
    created_utc = models.DateTimeField()
    karma = models.IntegerField()
    has_verified_email = models.BooleanField()
    extraction_date = models.DateTimeField()

class Subreddit(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    n_subscribers = models.IntegerField()
    created_utc = models.DateTimeField()
    over_18 = models.BooleanField()
    extraction_date = models.DateTimeField()

class Submission(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    selftext = models.TextField()
    created_utc = models.DateTimeField()
    distinguished = models.CharField(max_length=10)
    spoiler = models.BooleanField()
    allow_live_comments = models.BooleanField()
    is_video = models.BooleanField()
    media_only = models.BooleanField()
    is_self = models.BooleanField()
    is_original_content = models.BooleanField()
    link_flair_text = models.CharField(max_length=10)
    num_comments = models.IntegerField()
    over_18 = models.BooleanField()
    permalink = models.CharField(max_length=255)
    score = models.IntegerField()
    url = models.CharField(max_length=300)
    edited = models.BooleanField()
    upvote_ratio = models.FloatField()
    extraction_date = models.DateTimeField()
    # treatment_tags

class TreatmentTags(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.SET_NULL, null=True)

class Comment(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.SET_NULL, null=True)
    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True)
    parent_id = models.CharField(max_length=15)
    body = models.TextField()
    created_utc = models.DateTimeField()
    distinguished = models.BooleanField()
    is_submitter = models.BooleanField()
    score = models.IntegerField()
    link_flair_text = models.CharField(max_length=1024)
    extraction_date = models.DateTimeField()