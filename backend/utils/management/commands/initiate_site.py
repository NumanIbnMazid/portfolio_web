from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def _update_default_site(self):

        domain = settings.SITE_DOMAIN

        qs = Site.objects.all()

        if qs.exists():
            print("Updating site configuration...")
            qs.update(domain=domain, name=domain)
            print('Updated successfully...')
        else:
            print("Creating site configuration...")
            Site.objects.create(domain=domain, name=domain)
            print('Created successfully...')

    def handle(self, *args, **options):

        self._update_default_site()
