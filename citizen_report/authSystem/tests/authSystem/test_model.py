from django.contrib.auth import get_user_model
from django.test import TestCase

from ...const import Department

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.credentials_user = {
            'username': 'testUser',
            'email': 'test@gmail.com',
            'password': '12345'}
        self.credentials_clerk = {
            'username': 'testClerk',
            'email': 'testClerk@gmail.com',
            'password': '12345',
            'department': Department.GAS,
            'is_staff':True}
        self.credentials_admin = {
            'username': 'testAdmin',
            'email': 'testAdmin@gmail.com',
            'password': '12345'}

        self.user = User.objects.create_user(**self.credentials_user)
        self.clerk = User.objects.create_user(**self.credentials_clerk)
        self.admin = User.objects.create_superuser(**self.credentials_admin)

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))

    def test_user_username(self):
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, 'testUser')

    def test_user_email(self):
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.email, 'test@gmail.com')

    def test_user_department(self):
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.department, 'Department.APP')

    def test_user_is_clerk(self):
        user = User.objects.get(id=self.clerk.id)
        self.assertEqual(user.department, 'Department.GAS')
        self.assertTrue(user.is_staff == True)

    def test_user_is_admin(self):
        user = User.objects.get(id=self.admin.id)
        self.assertEqual(user.department, 'Department.SYS')
        self.assertTrue(user.is_superuser == True)

    def test_object_string(self):
        user = User.objects.get(id=self.user.id)
        expected_object_name = (f'Email: {user.email} '
                                f'Username: {user.username}')
        self.assertEqual(str(user), expected_object_name)
