from django.contrib.auth import get_user_model
from django.test import TestCase

from ...const import Department
from ...forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class FormUserTest(TestCase):
    def setUp(self):
        self.data_user = {'email': 'test@gmail.com', 'username': 'testUser', 'password1': 'testowehaslo432', 'password2': 'testowehaslo432'}
        self.blank_data = {}
        self.invalid_email_data = {'email': 'test', 'username': 'testUser', 'password1': 'testowehaslo432', 'password2': 'testowehaslo432'}
        self.invalid_password_data = {'email': 'test@gmail.com', 'username': 'testUser', 'password1': 'testowehaslo', 'password2': 'testowehaslo432'}

    def test_create_form_user(self):
        form = CustomUserCreationForm(data=self.data_user)
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        form = CustomUserCreationForm(data=self.blank_data)
        self.assertFalse(form.is_valid())

    def test_invalid_email_form(self):
        form = CustomUserCreationForm(data=self.invalid_email_data)
        self.assertFalse(form.is_valid())

    def test_invalid_password_form(self):
        form = CustomUserCreationForm(data=self.invalid_password_data)
        self.assertFalse(form.is_valid())


class FormUpdateUserTest(TestCase):
    def setUp(self):
        self.data_user = {'email': 'test@gmail.com', 'username': 'testUser'}
        self.blank_data = {}
        self.invalid_data = {'email': 'test', 'username': 'test User'}

    def test_update_form_user(self):
        form = CustomUserChangeForm(data=self.data_user)
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        form = CustomUserCreationForm(data=self.blank_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form(self):
        form = CustomUserChangeForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())