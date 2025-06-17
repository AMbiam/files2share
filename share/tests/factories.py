import factory
from factory import fuzzy as textgen #Generates text

from django.contrib.auth.models import User #import user model
from django.contrib.auth.hashers import make_password #Make password hashes, instead of saving as raw string.

from share.models.file import File
from share.models.access import Access


'''
When creating factories and sub factories,
the top down order of classese matter.  Any
class that requires a subfactory must be place 
below the factory class it uses.
'''

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f"user_{n:04}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")
    password = factory.LazyFunction(lambda: make_password('password'))


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = File
    title = textgen.FuzzyText(length=80)
    filename = textgen.FuzzyText(length=80)
    user = factory.SubFactory(UserFactory)

class AccessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Access
    fileobj = factory.SubFactory(FileFactory)
    filecode = textgen.FuzzyText(length=12)
    accesscode = textgen.FuzzyText(length=20)
    #Should be auto populated
    #attempts = 3
    #attempt_count = 0