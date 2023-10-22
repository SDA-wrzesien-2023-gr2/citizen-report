from django.contrib.auth import get_user_model
from django.test import TestCase

from ...models import NewsPost, NewsComment
from authSystem.const import Department
from report.models import Report
from report.constants import Category

User = get_user_model()


class NewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_user(
            username='testClerk', email='testClerk@gmail.com', password='12345', is_staff=True, department=Department.POW
        )
        self.report = Report.objects.create(
            title='Test Report', text='This is a report', category=Category.POWER_SUPPLY,
            user=self.user, clerk=self.clerk
        )
        self.news = NewsPost.objects.create(
            title='Test News', text='This is a news',
            clerk=self.clerk, report=self.report
        )

    def test_news_creation(self):
        self.assertTrue(isinstance(self.news, NewsPost))

    def test_news_title(self):
        news = NewsPost.objects.get(id=self.news.id)
        self.assertEqual(news.title, 'Test News')

    def test_news_text(self):
        news = NewsPost.objects.get(id=self.news.id)
        self.assertEqual(news.text, 'This is a news')

    def test_news_report(self):
        news = NewsPost.objects.get(id=self.news.id)
        self.assertEqual(news.report, self.report)

    def test_object_string(self):
        news = NewsPost.objects.get(id=self.news.id)
        expected_object_name = f'{news.title} | {news.created_at}'
        self.assertEqual(str(news), expected_object_name)


class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_user(
            username='testClerk', email='testClerk@gmail.com', password='12345', is_staff=True, department=Department.POW
        )
        self.report = Report.objects.create(
            title='Test Report', text='This is a report', category=Category.POWER_SUPPLY,
            user=self.user, clerk=self.clerk
        )
        self.news = NewsPost.objects.create(
            title='Test News', text='This is a news',
            clerk=self.clerk, report=self.report
        )
        self.comment = NewsComment.objects.create(
            text='This is a comment',
            user=self.user, post=self.news
        )

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, NewsComment))

    def test_comment_text(self):
        comment = NewsComment.objects.get(id=self.comment.id)
        self.assertEqual(comment.text, 'This is a comment')

    def test_comment_post(self):
        comment = NewsComment.objects.get(id=self.comment.id)
        self.assertEqual(comment.post, self.news)

    def test_object_string(self):
        comment = NewsComment.objects.get(id=self.comment.id)
        expected_object_name = f'Comment {comment.text} by {comment.user}'
        self.assertEqual(str(comment), expected_object_name)