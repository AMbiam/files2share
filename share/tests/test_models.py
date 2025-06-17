#from django.contrib.auth.models import User
import pytest

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from share.models.file import File

from pytest_django.asserts import assertTemplateUsed
from share.tests.factories import UserFactory


@pytest.fixture
def logged_user(client):
    user = UserFactory() #Use a factory user.
    client.login(username=user.username, password='password')
    return user


@pytest.mark.django_db
def test_create_user():
    user1 = User.objects.create_user(username='testuser1',password='teststring1')    
    #user1.save()

    assert 0 != user1.id


@pytest.mark.django_db
def test_create_user_same_username():
    user1 = User.objects.create_user(username='testuser1',password='teststring1')    
    #user1.save()

    assert 0 != user1.id

    with pytest.raises(IntegrityError) as exception_info:
        user2 = User.objects.create_user(username='testuser1',password='teststring1')
        #user2.save()

