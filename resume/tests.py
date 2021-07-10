import logging

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Resume

logging.disable(logging.CRITICAL)

ADMIN_NAME = 'admin'
ADMIN_PASS = 'password'
REGULAR_USER_NAME = 'user'
REGULAR_USER_PASS = 'example'
RESUME_DESCRIPTION = 'Python Developer'
RESUME_DESCRIPTION_MAX_LENGTH = Resume._meta.get_field(
    'description').max_length


class ResumeViewsTests(TestCase):

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            ADMIN_NAME, email=None, password=ADMIN_PASS)
        self.regular_user = get_user_model().objects.create_user(
            REGULAR_USER_NAME, password=REGULAR_USER_PASS)

    def tearDown(self):
        self.admin.delete()
        self.regular_user.delete()

    def test_anonymouse_user_submit_resume(self):
        response = self.client.post(
            '/resume/new', {'description': RESUME_DESCRIPTION})
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/resumes/')
        self.assertNotContains(response, f'{RESUME_DESCRIPTION}')

    def test_admin_submit_resume(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            '/resume/new', {'description': RESUME_DESCRIPTION})
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/resumes/')
        self.assertNotContains(
            response, f'{self.admin.username}: {RESUME_DESCRIPTION}')

    def test_regular_user_submit_invalid_resume(self):
        self.client.force_login(self.regular_user)
        invalid_description = 'a' * (RESUME_DESCRIPTION_MAX_LENGTH + 1)
        response = self.client.post(
            '/resume/new', {'description': invalid_description})
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/resumes/')
        self.assertNotContains(
            response, f'{self.regular_user.username}: {invalid_description}')

    def test_regular_user_submit_resume(self):
        self.client.force_login(self.regular_user)
        response = self.client.post(
            '/resume/new', {'description': RESUME_DESCRIPTION})
        self.assertRedirects(response, '/home')

        response = self.client.get('/resumes/')
        self.assertContains(
            response, f'{self.regular_user.username}: {RESUME_DESCRIPTION}')
