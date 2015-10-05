import factory
import random
import string

from django.contrib.auth import get_user_model
User = get_user_model()

def get_random_string(length=10):
    return 'u'.join(random.choice(string.ascii_letters) for part_of_string in range(length))

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda model: get_random_string())
    email = factory.LazyAttribute(lambda model: get_random_string() + "@" + get_random_string())
