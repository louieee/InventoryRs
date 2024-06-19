from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse


class LoginViewTestCase(APITestCase):

	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass')
		self.url = reverse('login')  # replace 'login' with the actual name of your login URL

	def test_valid_login(self):
		data = {
			'username': 'testuser',
			'password': 'testpass'
		}
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('token', response.data)
		token = Token.objects.get(key=response.data['token'])
		self.assertEqual(token.user, self.user)

	def test_invalid_username(self):
		data = {
			'username': 'wronguser',
			'password': 'testpass'
		}
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertIn('detail', response.data)
		self.assertEqual(response.data['detail'], 'You have no account with us')

	def test_invalid_password(self):
		data = {
			'username': 'testuser',
			'password': 'wrongpass'
		}
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertIn('detail', response.data)
		self.assertEqual(response.data['detail'], 'Incorrect Password')


class ChangePasswordViewTestCase(APITestCase):

	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='old_password')
		self.token = Token.objects.create(user=self.user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
		self.url = reverse('change-password')  # replace 'change_password' with the actual name of your URL

	def test_valid_change_password(self):
		data = {
			'old_password': 'old_password',
			'new_password': 'new_password123'
		}
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('new_password123'))

	def test_invalid_old_password(self):
		data = {
			'old_password': 'wrong_old_password',
			'new_password': 'new_password123'
		}
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('non_field_errors', response.data)
		self.assertEqual(response.data['non_field_errors'][0], 'Incorrect Password')
