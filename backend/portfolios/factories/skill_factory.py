import factory
from portfolios.models import Skill
from users.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory
from utils.helpers import create_factory_data


class SkillFactory(DjangoModelFactory):
    class Meta:
        model = Skill

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('word')
    image = factory.django.ImageField(color='blue')


def create_skills_with_factory(
    num_of_data=7, display_name="skill", display_name_plural="skills", delete_old_data=False
):

    return create_factory_data(
        factory=SkillFactory,
        num_of_data=num_of_data,
        display_name=display_name,
        display_name_plural=display_name_plural,
        delete_old_data=delete_old_data,
        model=Skill
    )
