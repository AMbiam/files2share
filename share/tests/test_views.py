#from django.contrib.auth.models import User
import pytest


from pytest_django.asserts import assertTemplateUsed
from share.tests.factories import UserFactory


@pytest.fixture
def public_urls():
    urls = [
        '/',
        '/share/download/',
    ]
    return urls

@pytest.fixture
def private_urls():
    urls = [
        '/share/upload/',
        '/share/files/',
    ]
    return urls

@pytest.fixture
def logged_user(client):
    user = UserFactory() #Use a factory user.
    client.login(username=user.username, password='password')
    return user

def test_pages_are_functioning(client, public_urls):
    for url in public_urls:
        response = client.get(path=url, follow=True)
        assert 200 == response.status_code


def test_pages_are_functioning_authenticated(client, private_urls):
    for url in private_urls:
        response = client.get(path=url, follow=False)
        assert 302 == response.status_code


@pytest.mark.django_db
def test_pages_are_functioning_authenticated_with_user(client, logged_user, private_urls):
    for url in private_urls:
        response = client.get(path=url, follow=False)
        assert 200 == response.status_code