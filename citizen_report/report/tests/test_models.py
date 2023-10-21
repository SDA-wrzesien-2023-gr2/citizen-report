from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Report
from ..utils import assign_clerk
from ..constants import Category

User = get_user_model()


class ReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser', email='test@gmail.com', password='12345'
        )
        self.clerk = User.objects.create_superuser(
            username='testClerk', email='testClerk@gmail.com', password='12345'
        )
        self.report = Report.objects.create(
            title='Test Report', text='This is a test', category=Category.POWER_SUPPLY,
            user=self.user, clerk=self.clerk
        )

    def test_report_creation(self):
        self.assertTrue(isinstance(self.report, Report))

    def test_report_title(self):
        report = Report.objects.get(id=self.report.id)
        self.assertEqual(report.title, 'Test Report')

    def test_report_text(self):
        report = Report.objects.get(id=self.report.id)
        self.assertEqual(report.text, 'This is a test')

    def test_report_category(self):
        report = Report.objects.get(id=self.report.id)
        self.assertEqual(report.category, 'POW')

    def test_object_string(self):
        report = Report.objects.get(id=self.report.id)
        expected_object_name = f'{report.title} | {report.updated_at}'
        self.assertEqual(str(report), expected_object_name)
