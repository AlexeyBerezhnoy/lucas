from django.core.management import BaseCommand, CommandError
from django.template.loader import render_to_string
from account.models import Moderator
from account.views import get_new_password
from account.views import send_message


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        try:
            moderator = Moderator.objects.get(email=options['email'])
        except:
            raise CommandError('Пользователь с адресом %s не найден' % options['email'])

        password = get_new_password()
        moderator.set_password(password)
        moderator.save()
        subject = "Пароль обновлён"
        ctx = {'user': moderator, 'password': password}
        message = render_to_string('account/email/new_password.html', ctx)
        send_message(options['email'], subject, message)
