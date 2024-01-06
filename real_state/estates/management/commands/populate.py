import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from mixer.backend.django import mixer
from users.models import User

from real_state.mongodb import mongodb


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-n",
            "--number",
            type=int,
            nargs="+",
            help="Number of users to create",
        )

    def handle(self, *args, **kwargs):
        """Populate MongoDB with estates and Postgres with users"""
        print("Populating MongoDB and Postgres")
        number = kwargs.get("number") or 10
        passwords = [mixer.faker.password() for _ in range(number)]
        user_emails = [mixer.faker.email() for _ in range(number)]

        print(f"Creating {number} users")
        # Create a csv file with the users and passwords
        with open(settings.CSV_FILE_PATH, "a") as f:
            for email, password in zip(user_emails, passwords):
                User.objects.create_user(email=email, password=password)
                f.write(f"email: {email}, password: {password}\n")

        print(f"Created {number} users!")

        # Create estates
        assets = pd.read_csv("assets.csv")
        assets.dropna(subset=["id"], inplace=True)

        assets = assets.to_dict(orient="records")
        # Remove all the Nan of the dict
        for asset in assets:
            for key, value in asset.items():
                if pd.isna(value):
                    asset[key] = None

        assets = assets[:10]

        print(f"Creating {len(assets)} estates")
        mongodb.update_many_estates(assets)
        print(f"Created {len(assets)} estates")
