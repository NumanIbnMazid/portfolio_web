from portfolios.factories.testimonial_factory import create_testimonials_with_factory
from django.db import transaction
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates dummy data"

    def _generate_dummy_data(self):
        # Create dummy data
        create_testimonials_with_factory(
            num_of_data=7,
            delete_old_data=False
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # generate data
        self._generate_dummy_data()
