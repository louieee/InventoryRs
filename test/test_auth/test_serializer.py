from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from api.v1.auth.serializer import LoginSerializer, ChangePasswordSerializer


class LoginSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.serializer = LoginSerializer()

    def test_valid_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        token_key = serializer.login()
        self.assertIsNotNone(token_key)
        token = Token.objects.get(key=token_key)
        self.assertEqual(token.user, self.user)

    def test_invalid_username(self):
        data = {
            'username': 'wronguser',
            'password': 'testpass'
        }
        serializer = LoginSerializer(data=data)
        with self.assertRaises(AuthenticationFailed) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(str(cm.exception.detail), 'You have no account with us')

    def test_invalid_password(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        serializer = LoginSerializer(data=data)
        with self.assertRaises(AuthenticationFailed) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(str(cm.exception.detail), 'Incorrect Password')



class ChangePasswordSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='old_password')
        self.serializer = ChangePasswordSerializer(instance=self.user)

    def test_valid_change_password(self):
        data = {
            'old_password': 'old_password',
            'new_password': 'new_password123'
        }
        serializer = ChangePasswordSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password123'))

    def test_invalid_old_password(self):
        data = {
            'old_password': 'wrong_old_password',
            'new_password': 'new_password123'
        }
        serializer = ChangePasswordSerializer(instance=self.user, data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
