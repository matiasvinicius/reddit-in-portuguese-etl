from extraction.models import Subreddit
from django.core.management.base import BaseCommand
from extraction.lib.praw_utils import create_praw_instace
from django.apps import apps
from datetime import datetime, timezone

class Command(BaseCommand):
    help = 'Create Subreddit objects based on a list of subreddit names'

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="file path")

    def handle(self, *args, **options):
        file_path = options["path"]
        reddit = create_praw_instace()

        if not file_path.endswith(".txt"):
            print("subreddit names must be in a txt file")
            quit()
        
        for i, subreddit_name in enumerate(open(file_path, "r").read().splitlines()):
            print(f"Subreddit {i+1} - {subreddit_name}")
            subreddit_metadata = reddit.subreddit(subreddit_name)
            
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
