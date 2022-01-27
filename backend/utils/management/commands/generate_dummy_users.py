from django.contrib.auth import get_user_model
from users.factories.user_factory import create_users_with_factory
from django.db import transaction
from django.core.management.base import BaseCommand


info = {
    "NUM_OF_DATA": 7,
    "MODEL": get_user_model(),
    "DELETE_OLD_DATA": False,
}


class Command(BaseCommand):
    help = "Generates dummy data"

    def _generate_dummy_data(self):
        # Create dummy data
        create_users_with_factory(
            num_of_data=info.get("NUM_OF_DATA"),
            delete_old_data=info.get("DELETE_OLD_DATA")
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # generate data
        self._generate_dummy_data()
