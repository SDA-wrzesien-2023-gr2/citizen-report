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
        response = self.client.get(self.urlList, kwargs={"pk": self.reports[1].pk})
        # for report 'Test Report Gas' there is only one news
        self.assertQuerysetEqual(response.context['newspost_list'], [self.news[0]])

    def test_news_pagination(self):
        self.urlList = reverse('news', kwargs={"pk": self.reports[0].pk})
        response = self.client.get(self.urlList, kwargs={"pk": self.reports[0].pk})
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)

    def test_news_pagination_is_two(self):
        self.urlList = reverse('news', kwargs={"pk": self.reports[0].pk})
        response = self.client.get(self.urlList, kwargs={"pk": self.reports[0].pk})
        self.assertEqual(len(response.context['newspost_list']), 2)

    def test_news_correct_template(self):
        self.urlList = reverse('news', kwargs={"pk": self.reports[0].pk})
        response = self.client.get(self.urlList, kwargs={"pk": self.reports[0].pk})
        self.assertTemplateUsed(response, 'news.html')
