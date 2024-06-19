from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction


class Command(BaseCommand):
	help = 'Create an employee'

	@transaction.atomic
	def handle(self, *args, **kwargs):
		first_name = input("Enter Employee's firstname: ")
		last_name = input("Enter Employee's lastname: ")
		correct_username = False
		correct_email = False
		while not correct_username:
			username = input("Enter Employee's username: ")
			correct_username = not User.objects.filter(username=username).exists()
			if not correct_username:
				self.stdout.write(self.style.ERROR('User with this username already exists.'))
		while not correct_email:
			email = input("Enter Employee's email: ")
			correct_email = not User.objects.filter(email=email).exists()
			if not correct_email:
				self.stdout.write(self.style.ERROR('User with this username already exists.'))
		password = "Start12345"




		User.objects.create_user(username=username, email=email, password=password, is_staff=True,
		                         first_name=first_name, last_name=last_name)
		self.stdout.write(self.style.SUCCESS(f'Successfully created an employee with username "{username}"; your password is {password}'))
