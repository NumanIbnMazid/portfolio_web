import factory
from portfolios.models import Interest
from users.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory
from utils.helpers import create_factory_data


class InterestFactory(DjangoModelFactory):
    class Meta:
        model = Interest

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('word')
    icon = factory.django.ImageField(color='blue')
    description = factory.Faker('text')


def create_interests_with_factory(
    num_of_data=7, display_name="interest",
    display_name_plural="interests", delete_old_data=False
):

    return create_factory_data(
        factory=InterestFactory,
        num_of_data=num_of_data,
        display_name=display_name,
        display_name_plural=display_name_plural,
        delete_old_data=delete_old_data,
        model=Interest
    )
