from django.contrib.auth import get_user_model
from users.factories.user_factory import create_users_with_factory
from django.db import transaction
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates dummy data"

    def _generate_dummy_data(self):
        # Create dummy data
        create_users_with_factory(
            num_of_data=7,
            delete_old_data=False
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # generate data
        self._generate_dummy_data()
