import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from utils.helpers import create_factory_data


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    name = factory.Faker("first_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'test12345')


def create_users_with_factory(num_of_data=7, display_name="user", display_name_plural="users", delete_old_data=False):

    return create_factory_data(
        factory=UserFactory,
        num_of_data=num_of_data,
        display_name=display_name,
        display_name_plural=display_name_plural,
        delete_old_data=delete_old_data,
        model=get_user_model()
    )
