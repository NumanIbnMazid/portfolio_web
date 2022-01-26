from portfolios.models import Skill
from portfolios.factory import SkillFactory
from django.db import transaction
from django.core.management.base import BaseCommand


NUM_OF_DATA = 7

info = {
    "model": Skill,
    "factory": SkillFactory,
    "display": "Skill",
    "display_plural": "Skills",
    "delete_old_data": False
}


class Command(BaseCommand):
    help = "Generates dummy data"

    def _delete_old_data(self):
        info.get("model").objects.all().delete()
        self.stdout.write("Deleted old data...")

    def _generate_dummy_data(self):
        self.stdout.write(f"Creating {info.get('display_plural')}...")
        # Create dummy data
        data = []
        for _ in range(NUM_OF_DATA):
            self.stdout.write(f"Creating {info.get('display')}: {_ + 1}")
            instance = info.get("factory")()
            data.append(instance)
        self.stdout.write(f"Created {info.get('display_plural')}...")

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # delete old data
        if info.get("delete_old_data"):
            self._delete_old_data()
        # create new data
        self._generate_dummy_data()
