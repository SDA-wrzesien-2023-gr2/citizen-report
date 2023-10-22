from django.contrib.auth import get_user_model
from django.test import TestCase

from ...forms import NewsForm, NewsCommentForm

User = get_user_model()


class FormNewsTest(TestCase):
    def setUp(self):
        self.data = {'title': 'Test form', 'text': 'Text test'}
        self.invalid_data = {'title': '', 'text': 'Text test'}

    def test_create_news_form(self):
        form = NewsForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_news_form(self):
        form = NewsForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())


class FormCommentTest(TestCase):
    def setUp(self):
        self.data = {'text': 'Text test'}
        self.invalid_data = {'text': ''}

    def test_create_news_form(self):
        form = NewsCommentForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_news_form(self):
        form = NewsCommentForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())