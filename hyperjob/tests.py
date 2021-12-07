import logging

from django.contrib.auth import get_user_model
from django.test import TestCase

logging.disable(logging.CRITICAL)

ADMIN_NAME = 'admin'
ADMIN_PASS = 'password'
REGULAR_USER_NAME = 'user'
REGULAR_USER_PASS = 'secret'


class BaseTestCase(TestCase):

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            ADMIN_NAME, email=None, password=ADMIN_PASS)
        self.regular_user = get_user_model().objects.create_user(
            REGULAR_USER_NAME, password=REGULAR_USER_PASS)

    def tearDown(self):
        self.admin.delete()
        self.regular_user.delete()


class MainViewTests(BaseTestCase):

    def test_anonymouse_user_greeting(self):
        response = self.client.get('/')
        self.assertContains(response, 'Welcome to HyperJob, Guest')

    def test_authenticated_user_greeting(self):
        self.client.force_login(self.regular_user)
        response = self.client.get('/')
        self.assertContains(
            response, f'Welcome to HyperJob, {self.regular_user.username}')


class HomeViewTests(BaseTestCase):

    def test_anonymouse_user_greeting(self):
        response = self.client.get('/home')
        self.assertContains(response, 'Hello, <b>Guest</b>')

    def test_authenticated_admin_greeting(self):
        self.client.force_login(self.admin)
        response = self.client.get('/home')
        self.assertContains(response, f'Hello, <b>{self.admin.username}</b>')
        self.assertContains(response, 'Create new vacancy')

    def test_authenticated_user_greeting(self):
        self.client.force_login(self.regular_user)
        response = self.client.get('/home')
        self.assertContains(
            response, f'Hello, <b>{self.regular_user.username}</b>')
        self.assertContains(response, 'Create new resume')
