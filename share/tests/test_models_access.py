#from django.contrib.auth.models import User
import pytest

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from share.models import File, Access

from share.tests.factories import UserFactory, FileFactory, AccessFactory


@pytest.fixture
def created_user():
    user1 = UserFactory()    
    return user1

@pytest.fixture
def access_credentials():
    return {'u' : 'randomuser', 'p' : 'testing'}


#Testing File creation
@pytest.mark.django_db
def test_create_file_access(created_user):
    access = AccessFactory(fileobj=FileFactory(user=created_user))
    assert 0 != access.id
    assert 0 != access.fileobj.id
    assert 0 != access.fileobj.user.id


@pytest.mark.django_db
def test_create_file_access_then_query(created_user, access_credentials):
    fileobj = FileFactory(user=created_user)
    access = AccessFactory(fileobj=fileobj, filecode=access_credentials['u'], accesscode=access_credentials['p'])

    accesses = Access.objects.filter(filecode=access_credentials['u'], accesscode=access_credentials['p']).values()
    assert 1 == len(accesses)
    
@pytest.mark.django_db
def test_create_file_access_then_query(created_user, access_credentials):
    fileobj = FileFactory(user=created_user)
    access1 = AccessFactory(fileobj=fileobj, filecode=access_credentials['u'], accesscode=access_credentials['p'])

    with pytest.raises(IntegrityError) as exception_info:
        access2 = AccessFactory(fileobj=fileobj, filecode=access_credentials['u'], accesscode=access_credentials['p']) #Should throw a constraint exception



