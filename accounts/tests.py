from django.test import TestCase
from .serializers import RegistrationSerializer


class RegistrationSerializerTestCase(TestCase):

    def test_valid_serializer(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.first_name, data['first_name'])

    def test_non_matching_passwords(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'password': 'testpass123',
            'password2': 'wrongtestpass123',
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password2', serializer.errors)
