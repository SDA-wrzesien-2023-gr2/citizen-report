from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.shortcuts import render

from report.models import Report

from report.constants import Category
from authSystem.const import Department
from ...views import NewsPostCreate, NewsCommentCreate
from ...models import NewsPost, NewsComment

User = get_user_model()


class ReadNewsListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerks = [
            User.objects.create_user(
                username='testClerkPow', email='testClerk1@gmail.com', password='12345',
                is_staff=True, department=Department.POW),
            User.objects.create_user(
                username='testClerkGas', email='testClerk2@gmail.com', password='12345',
                is_staff=True, department=Department.GAS),

        ]
        self.reports = [
            Report.objects.create(
                title='Test Report Pow', text='This is a test', category=Category.POWER_SUPPLY,
                user=self.user, clerk=self.clerks[0]),
            Report.objects.create(
                title='Test Report Gas', text='This is a test', category=Category.GASWORKS,
                user=self.user, clerk=self.clerks[1])
        ]
        self.news = [
            NewsPost.objects.create(
                title='Test News POW 1', text='This is a news',
                clerk=self.clerks[0], report=self.reports[0]),
            NewsPost.objects.create(
                title='Test News POW 2', text='This is a news',
                clerk=self.clerks[0], report=self.reports[0]),
            NewsPost.objects.create(
                title='Test News POW 3', text='This is a news',
                clerk=self.clerks[0], report=self.reports[0]),
            NewsPost.objects.create(
                title='Test News GAS 1', text='This is a news',
                clerk=self.clerks[1], report=self.reports[1]),
        ]
        self.news.reverse()

    def test_news_accessible(self):
        self.urlList = reverse('news', kwargs={"pk": self.reports[0].pk})
        response = self.client.get(self.urlList)
        self.assertEqual(response.status_code, 200)

    def test_news_power_reports(self):
        self.urlList = reverse('news', kwargs={"pk": self.reports[1].pk})
        response = self.client.get(self.urlList)
        # for report 'Test Report Gas' there is only one news
        self.assertQuerysetEqual(response.context['newspost_list'], [self.news[0]])

    def test_news_pagination(self):
        self.urlList = reverse('news', kwargs={"pk": self.reports[0].pk})
        response = self.client.get(self.urlList)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)

    def test_news_pagination_is_two(self):
        self.urlList = reverse('news', kwargs={"pk": self.reports[0].pk})
        response = self.client.get(self.urlList)
        self.assertEqual(len(response.context['newspost_list']), 2)

    def test_news_correct_template(self):
        self.urlList = reverse('news', kwargs={"pk": self.reports[0].pk})
        response = self.client.get(self.urlList)
        self.assertTemplateUsed(response, 'news.html')


class ReadDetailNewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_user(
            username='testClerk', email='testClerk@gmail.com', password='12345', is_staff=True,
            department=Department.POW
        )
        self.report = Report.objects.create(
            title='Test Report 1', text='This is a text', category=Category.POWER_SUPPLY,
            user=self.user, clerk=self.clerk)
        self.news = NewsPost.objects.create(title='Test News', text='This is a news',
                                            clerk=self.clerk, report=self.report)
        self.comment = NewsComment.objects.create(text='This is a comment',
                                                  user=self.user, post=self.news, approved_comment=True)

        self.url = reverse('detail_news', kwargs={'pk': self.news.pk})

    def test_detail_news(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_text_news(self):
        response = self.client.get(self.url)
        self.assertContains(response, "is a news")

    def test_detail_news_have_comment(self):
        response = self.client.get(self.url)
        self.assertTrue(response.context['newspost'].comments)


class CreateNewsPostTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_user(
            username='testClerk', email='testClerk@gmail.com', password='12345', is_staff=True,
            department=Department.POW
        )
        self.report = Report.objects.create(
            title='Test Report 1', text='This is a text', category=Category.POWER_SUPPLY,
            user=self.user, clerk=self.clerk)
        self.data = {'title': 'Test News', 'text': 'This is news.'}
        self.url = reverse('create_news', kwargs={'pk': self.report.pk})

    def test_create_news(self):
        self.client.force_login(self.clerk)
        request = self.factory.post(self.url, self.data)
        request.user = self.clerk
        kwargs = {'pk': self.report.pk}
        response = NewsPostCreate.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

    def test_create_news_deny_not_login(self):
        response = self.client.post(self.url, self.data, kwargs={'pk': self.report.pk})
        self.assertRedirects(response, f'/admin/login/?next=/reports/{self.report.id}/create-news/')

    def test_create_news_deny_not_clerk(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data, kwargs={'pk': self.report.pk})
        self.assertRedirects(response, f'/admin/login/?next=/reports/{self.report.id}/create-news/')

    def test_create_news_fail_blank(self):
        self.client.force_login(self.clerk)
        response = self.client.post(self.url, {})
        self.assertFormError(response, 'form', 'title', 'This field is required.')


class CreateNewsCommentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_user(
            username='testClerk', email='testClerk@gmail.com', password='12345', is_staff=True,
            department=Department.POW
        )
        self.report = Report.objects.create(
            title='Test Report 1', text='This is a text', category=Category.POWER_SUPPLY,
            user=self.user, clerk=self.clerk)
        self.news = NewsPost.objects.create(
            title='Test News', text='This is a news', clerk=self.clerk, report=self.report)
        self.data = {'text': 'This is test comment'}
        self.url = reverse('add_comment_to_news', kwargs={'pk': self.news.pk})

    def test_create_comment(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)

    def test_create_comment_deny_not_login(self):
        response = self.client.post(self.url, self.data, kwargs={'pk': self.news.pk})
        self.assertRedirects(response, f'/authSystem/login/?next=/news/{self.news.id}/comment/')

    def test_create_comment_fail_blank(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {})
        self.assertFormError(response, 'form', 'text', 'This field is required.')
