from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.shortcuts import render

from ...models import User
from ...const import Department
from ...views import SignUp


class SignupTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.data = {'email': 'test@gmail.com', 'username': 'testUser', 'password1': 'testowehaslo432',
                     'password2': 'testowehaslo432'}
        self.url = reverse('signup')

    def test_sign_up_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_signup_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'signup.html')

    def test_sign_up_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testUser').exists())

    def test_signup_fail_blank(self):
        response = self.client.post(self.url, {})
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_signup_invalid(self):
        response = self.client.post(self.url,
                                    {'email': 'invalidEmail', 'username': 'testUser.', 'password1': 'testowehaslo432',
                                     'password2': 'testowehaslo432'})
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')


class LogInTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='testowehaslo432'
        )
        self.data = {'username': 'testUser', 'password': 'testowehaslo432'}
        self.url = reverse('login')

    def test_sign_up_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_signup_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'login.html')

    def test_logged_in_user(self):
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)

    def test_login_fail_blank(self):
        response = self.client.post(self.url, {})
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_login_invalid(self):
        response = self.client.post(self.url,
                                    {'username': 'testUser', 'password': 'invalidPassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)


class ReadProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.url = reverse('profile')

    def test_detail_report(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_my_profile_deny_not_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/authSystem/login/?next=/authSystem/user/')

    def test_detail_text_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(response, f"Email: {self.user.email} ")


class ChangePasswordTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='testowehaslo432'
        )
        self.data = {'old_password': 'testowehaslo432', 'new_password1': 'nowehaslo432', 'new_password2': 'nowehaslo432'}
        self.url = reverse('change_password')


    def test_change_password_accessible(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_change_password_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user/change_password.html')

    def test_my_profile_deny_not_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/authSystem/login/?next=/authSystem/user/change_password/')

    def test_changed_user_password(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_form_fail_blank(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {})
        self.assertFormError(response, 'form', 'old_password', 'This field is required.')

    def test_form_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url,
                                    {'old_password': 'wrongPassword', 'new_password1': 'nowehaslo432', 'new_password2': 'nowehaslo432'})
        self.assertFormError(response, 'form', 'old_password',
                             'Your old password was entered incorrectly. Please enter it again.')


class ResetPasswordTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='testowehaslo432'
        )
        self.data = {'email': 'test@gmail.com'}
        self.url = reverse('reset_password')

    def test_reset_password_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user/reset_password.html')

    def test_reset_user_password(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_reset_fail_blank(self):
        response = self.client.post(self.url, {})
        self.assertFormError(response, 'form', 'email', 'This field is required.')

    def test_reset_invalid_data(self):
        response = self.client.post(self.url,
                                    {'email': 'testgmail.com'})
        self.assertFormError(response, 'form', 'email',
                             'Enter a valid email address.')
