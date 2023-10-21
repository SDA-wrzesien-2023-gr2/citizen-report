from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.shortcuts import render

from ..constants import Category, Status
from ..models import Report
from ..views import ReportCreate, update_status
from news.models import NewsPost

User = get_user_model()


class HomeTest(TestCase):
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
        ]
        self.news = [
            NewsPost.objects.create(
                title='Test News 1', text='This is a test', clerk=self.clerk, report=self.reports[0]),
            NewsPost.objects.create(
                title='Test News 2', text='This is a test', clerk=self.clerk, report=self.reports[0]),
        ]
        self.url= reverse('home')
        self.reports.reverse()
        self.news.reverse()

    def test_home_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_have_reports(self):
        response = self.client.get(self.url)
        # only last reports we have on home page
        self.assertQuerysetEqual(response.context['reports'], self.reports)

    def test_home_have_news(self):
        response = self.client.get(self.url)
        # only last reports we have on home page
        self.assertQuerysetEqual(response.context['news_list'], self.news)

    def test_home_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')


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
            Report.objects.create(
                title='Test Report 4', text='This is a test', category=Category.HEALTHCARE,
                user=self.user, clerk=self.clerk),
            Report.objects.create(
                title='Test Report 5', text='This is a test', category=Category.PUBLIC_SAFETY,
                user=self.user, clerk=self.clerk),
        ]
        self.urlList = reverse('reports')

    def test_list_accessible(self):
        response = self.client.get(self.urlList)
        self.assertEqual(response.status_code, 200)

    def test_list_reports_pagination(self):
        response = self.client.get(self.urlList)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)

    def test_list_reports_pagination_is_four(self):
        response = self.client.get(self.urlList)
        self.assertEqual(len(response.context['reports']), 4)

    def test_list_reports_correct_template(self):
        response = self.client.get(self.urlList)
        self.assertTemplateUsed(response, 'reports.html')

    def test_list_reports_query_search(self):
        self.urlListFilter = '{url}?{search}={value}'.format(
            url=reverse('reports'),
            search='search', value='1')
        response = self.client.get(self.urlListFilter)
        self.assertQuerysetEqual(response.context['reports'], [self.reports[0]])

    def test_list_reports_query_filter(self):
        self.urlListFilter = '{url}?{filter1}={value1}&{filter2}={value2}'.format(
            url=reverse('reports'),
            filter1='category', value1='GAS', filter2='status', value2='')
        response = self.client.get(self.urlListFilter)
        self.assertQuerysetEqual(response.context['reports'], [self.reports[1]])


class ReadMyReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk_pow = User.objects.create_superuser(
            username='testClerk Power', email='testClerkPow@gmail.com', password='12345'
        )
        self.clerk_gas = User.objects.create_superuser(
            username='testClerk Gasworks', email='testClerkGas@gmail.com', password='12345'
        )
        self.clerk_pub = User.objects.create_superuser(
            username='testClerk Safety', email='testClerkPub@gmail.com', password='12345'
        )
        self.clerk_pow.department = Category.POWER_SUPPLY
        self.clerk_gas.department = Category.GASWORKS
        self.clerk_pub.department = Category.PUBLIC_SAFETY
        self.reports = [
            Report.objects.create(
                title='Test Report 1', text='This is a test', category=Category.POWER_SUPPLY,
                user=self.user, clerk=self.clerk_pow),
            Report.objects.create(
                title='Test Report 2', text='This is a test', category=Category.GASWORKS,
                user=self.user, clerk=self.clerk_gas),
            Report.objects.create(
                title='Test Report 3', text='This is a test', category=Category.PUBLIC_SAFETY,
                user=self.user, clerk=self.clerk_pub),

        ]
        self.urlList = reverse('my_reports')
        self.reports.reverse()

    def test_my_reports_accessible(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urlList)
        self.assertEqual(response.status_code, 200)

    def test_my_reports_deny_not_login(self):
        response = self.client.get(self.urlList)
        self.assertRedirects(response, '/authSystem/login/?next=/my-reports/')

    def test_my_reports_login_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urlList)
        # user have 2 last reports because of pagination
        self.assertQuerysetEqual(response.context['reports'], self.reports[:2])

    def test_my_reports_login_clerk(self):
        self.client.force_login(self.clerk_pow)
        response = self.client.get(self.urlList)
        # clerk only have a report that is assigned to him
        self.assertQuerysetEqual(response.context['reports'], [self.reports[2]])

    def test_my_reports_user_pagination(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urlList)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)

    def test_my_reports_reports_pagination_is_two(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urlList)
        self.assertEqual(len(response.context['reports']), 2)

    def test_my_reports_reports_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urlList)
        self.assertTemplateUsed(response, 'my_reports.html')


class ReadDetailReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_superuser(
            username='testClerk', email='testClerk@gmail.com', password='12345'
        )
        self.report = Report.objects.create(
            title='Test Report 1', text='This is a text', category=Category.POWER_SUPPLY,
            user=self.user, clerk=self.clerk)
        self.url = reverse('detail', kwargs={'report_id': self.report.id})

    def test_detail_report(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_text_report(self):
        response = self.client.get(self.url)
        self.assertContains(response, "is a text")


class CreateReportTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_superuser(
            username='testClerk', email='testClerk@gmail.com', password='12345'
        )
        self.clerk.department = Category.POWER_SUPPLY
        self.data = {'title': 'Hello world', 'text': 'Something intrest.', 'category': Category.POWER_SUPPLY}
        self.url = reverse('create')

    def test_create_report(self):
        self.client.force_login(self.user)
        request = self.factory.post(self.url, self.data)
        request.user = self.user
        kwargs = {"clerk": self.clerk}
        response = ReportCreate.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

    def test_create_report_deny_not_login(self):
        response = self.client.post(self.url, self.data, kwargs={"clerk": self.clerk})
        self.assertRedirects(response, '/authSystem/login/?next=/create/')

    def test_create_report_fail_blank(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {})
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_create_report_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url,
                                    {'title': 'Hello world', 'text': 'Something intrest.', 'category': 'power'},
                                    kwargs={"clerk": self.clerk})
        self.assertFormError(response, 'form', 'category',
                             'Select a valid choice. power is not one of the available choices.')


class UpdateReportTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_superuser(
            username='testClerk', email='testClerk@gmail.com', password='12345'
        )
        self.report = Report.objects.create(
            title='Test Report 1', text='This is a text', category=Category.POWER_SUPPLY,
            user=self.user, clerk=self.clerk)
        self.data = {'status': Status.APPROVED}
        self.url = reverse('update_report', kwargs={'report_id': self.report.id})

    def test_update_report(self):
        self.client.force_login(self.clerk)
        request = self.factory.post(self.url, self.data)
        request.user = self.clerk
        response = update_status(request, report_id=self.report.id)
        self.assertEqual(response.status_code, 302)

    def test_update_report_deny_not_clerk(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_update_report_deny_not_login(self):
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, f'/authSystem/login/?next=/update-report/{self.report.id}/')

    def test_update_report_fail_blank(self):
        self.client.force_login(self.clerk)
        response = self.client.post(self.url, {})
        self.assertFormError(response, 'form', 'status', 'This field is required.')

    def test_update_report_invalid(self):
        self.client.force_login(self.clerk)
        response = self.client.post(self.url, {'status': 'considering'})
        self.assertFormError(response, 'form', 'status',
                             'Select a valid choice. considering is not one of the available choices.')
