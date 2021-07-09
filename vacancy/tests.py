# pylint: disable=redefined-outer-name, unused-argument
import logging

import pytest
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects

from .models import Vacancy

logging.disable(logging.CRITICAL)

ADMIN_NAME = 'admin'
ADMIN_PASS = 'password'
REGULAR_USER_NAME = 'user'
REGULAR_USER_PASS = 'example'
VACANCY_DESCRIPTION = 'Python Developer'
VACANCY_DESCRIPTION_MAX_LENGTH = Vacancy._meta.get_field(
    'description').max_length


@pytest.fixture
def admin(db, django_user_model):
    superuser = django_user_model.objects.create_superuser(
        ADMIN_NAME, email=None, password=ADMIN_PASS)
    yield superuser
    superuser.delete()


@pytest.fixture
def regular_user(db, django_user_model):
    user = django_user_model.objects.create_user(
        REGULAR_USER_NAME, password=REGULAR_USER_PASS)
    yield user
    user.delete()


@pytest.mark.django_db
class TestVacancyViews:

    def test_anonymouse_user_submit_vacancy(self, client):
        response = client.post(
            '/vacancy/new', {'description': VACANCY_DESCRIPTION})
        assert response.status_code == 403

        response = client.get('/vacancies/')
        assertNotContains(response, f'{VACANCY_DESCRIPTION}')

    def test_regular_user_submit_vacancy(self, client, regular_user):
        client.force_login(regular_user)
        response = client.post(
            '/vacancy/new', {'description': VACANCY_DESCRIPTION})
        assert response.status_code == 403

        response = client.get('/vacancies/')
        assertNotContains(
            response, f'{regular_user.username}: {VACANCY_DESCRIPTION}')

    def test_admin_submit_invalid_vacancy(self, client, admin):
        client.force_login(admin)
        invalid_description = 'a' * (VACANCY_DESCRIPTION_MAX_LENGTH + 1)
        response = client.post(
            '/vacancy/new', {'description': invalid_description})
        assert response.status_code == 400

        response = client.get('/vacancies/')
        assertNotContains(response, f'{admin.username}: {invalid_description}')

    def test_admin_submit_vacancy(self, client, admin):
        client.force_login(admin)
        response = client.post(
            '/vacancy/new', {'description': VACANCY_DESCRIPTION})
        assertRedirects(response, '/home')

        response = client.get('/vacancies/')
        assertContains(response, f'{admin.username}: {VACANCY_DESCRIPTION}')
