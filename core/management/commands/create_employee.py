from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.db import transaction
from django.utils.crypto import get_random_string



class Command(BaseCommand):
	help = 'Create an employee'

	# def add_arguments(self, parser):
	# 	parser.add_argument('--username', type=str, help='Indicates the username of the employee')
	# 	parser.add_argument('--email', type=str, help='Indicates the email of the employee')

	@transaction.atomic
	def handle(self, *args, **kwargs):
		username = input("Enter Employee's username: ")
		email = input("Enter Employee's email: ")
		password = "Start12345"

		if User.objects.filter(username=username).exists():
			self.stdout.write(self.style.ERROR('User with this username already exists.'))
		else:
			user = User.objects.create_user(username=username, email=email, password=password, is_staff=True)
			for model in ("item", "supplier"):
				content_type = ContentType.objects.filter(model=model).first()
				if content_type:
					permissions = Permission.objects.filter(content_type=content_type)
					user.user_permissions.add(*permissions)


			self.stdout.write(self.style.SUCCESS(f'Successfully created an employee with username "{username}"'))
