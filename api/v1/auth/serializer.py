from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()
	user = None

	def validate(self, attrs):
		user: User = User.objects.filter(username__iexact=attrs["username"]).first()
		if not user:
			raise AuthenticationFailed("You have no account with us")
		if not user.check_password(attrs["password"]):
			raise AuthenticationFailed("Incorrect Password")
		self.user = user
		return attrs

	def login(self):
		token, _ = Token.objects.get_or_create(user_id=self.user.id)
		return token.key


class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField()
	new_password = serializers.CharField()

	def validate(self, attrs):
		if not self.instance.check_password(attrs["old_password"]):
			raise ValidationError("Incorrect Password")
		return attrs

	def update(self, instance: User, validated_data):
		instance.set_password(validated_data.pop("new_password"))
		instance.save()
		return instance
