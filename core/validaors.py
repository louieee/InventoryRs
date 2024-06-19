import re

from django.core.exceptions import ValidationError


def phone_number_validator(value):
	"""
        Validates a phone number using a regular expression.
    """
	regex = r'\+[\d]{1,3}[\d]{0,15}'  # Adjust the regex for your phone number format
	if not re.match(regex, value):
		raise ValidationError("Invalid phone number format.")
