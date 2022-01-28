from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **options):

        if not get_user_model().objects.filter(
            email=os.environ.get('DJANGO_SU_EMAIL')
        ).exists():
            print('Creating django superuser ...')
            get_user_model().objects.create_superuser(
                email=os.environ.get('DJANGO_SU_EMAIL'),
                username=os.environ.get('DJANGO_SU_NAME'),
                password=os.environ.get('DJANGO_SU_PASSWORD')
            )
            print('Created successfully...')
        else:
            print(f"Admin ({os.environ.get('DJANGO_SU_EMAIL')}) already exists!")
