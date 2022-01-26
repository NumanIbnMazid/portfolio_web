import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from users.factory import UserFactory


class SkillFactory(DjangoModelFactory):
    class Meta:
        model = 'portfolios.Skill'

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('word')
    image = factory.django.ImageField(color='blue')
