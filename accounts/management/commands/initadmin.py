from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.WARNING('DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set. Skipping superuser creation.'))
            return

        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.SUCCESS(f'User {username} already exists. Updating password and permissions.'))
            user.email = email
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
        except User.DoesNotExist:
            self.stdout.write(self.style.SUCCESS(f'Creating superuser: {username}'))
            User.objects.create_superuser(username=username, email=email, password=password)
