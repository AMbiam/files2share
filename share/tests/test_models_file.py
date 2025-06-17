#from django.contrib.auth.models import User
import pytest

from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from share.models.file import File


from share.tests.factories import UserFactory, FileFactory


@pytest.fixture
def created_user():
    user1 = UserFactory()   
    return user1


#Testing File creation
@pytest.mark.django_db
def test_create_file_without_user():
    with pytest.raises(IntegrityError) as exception_info:
        file = File.objects.create(title="testfile", filename='testfilename.txt')
        file.save()


#Testing File creation
@pytest.mark.django_db
def test_create_file_with_user(created_user):

    file = File.objects.create(title="testfile", filename='testfilename.txt', user=created_user)

    #Getting all related objects.
    files = created_user.files.all()
    assert 1 == len(files)

#Testing File creation
@pytest.mark.django_db
def test_create_files_with_user(created_user):
    FileFactory.create_batch(4, user=created_user)
    FileFactory.create_batch(5)
    files = created_user.files.all()
    assert 4 == len(files)



