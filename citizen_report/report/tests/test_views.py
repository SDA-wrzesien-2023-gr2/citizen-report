from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.shortcuts import render

from ..constants import Category
from ..models import Report
from ..views import ReportCreate

User = get_user_model()


class ReadReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_superuser(
            username='testClerk', email='testClerk@gmail.com', password='12345'
        )
        self.reports = [
            Report.objects.create(
                title='Test Report 1', text='This is a test', category=Category.POWER_SUPPLY,
                user=self.user, clerk=self.clerk),
            Report.objects.create(
                title='Test Report 2', text='This is a test', category=Category.GASWORKS,
                user=self.user, clerk=self.clerk),
            Report.objects.create(
                title='Test Report 3', text='This is a test', category=Category.PUBLIC_SAFETY,
                user=self.user, clerk=self.clerk),
        ]
        self.urlList = reverse('reports')

    def test_list_reports(self):
        response = self.client.get(self.urlList)
        self.assertEqual(response.status_code,200)
        self.assertQuerySetEqual(response.context["reports"], self.reports)


class ReadDetailReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_superuser(
            username='testClerk', email='testClerk@gmail.com', password='12345'
        )
        self.report = Report.objects.create(
                title='Test Report 1', text='This is a test', category=Category.POWER_SUPPLY,
                user=self.user, clerk=self.clerk)
        self.url = reverse('detail',kwargs={'report_id':self.report.id})

    def test_detail_report(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "is a test")


class CreateReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_superuser(
            username='testClerk', email='testClerk@gmail.com', password='12345'
        )
        self.clerk.department=Category.POWER_SUPPLY

        self.data = {'title':'Hello world','text':'Something intrest.','category':Category.POWER_SUPPLY}
        # print(self.clerk.department)
        # print(self.clerk.is_staff)
        # print(User.objects.all())
        self.url = reverse('create')
        self.client.force_login(self.user)

    def test_create_report(self):
        request = self.client.post(ReportCreate, data=self.data, kwargs={'clerk': self.clerk} )
        response = ReportCreate.as_view()(request)
        # response = self.client.post(self.url, self.data, kwargs={'clerk': self.clerk})
        self.assertEqual(response.status_code, 201)