from django.core.management.base import BaseCommand
from account.models import MyUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('hii')

