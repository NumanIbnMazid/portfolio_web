import factory
from portfolios.models import Project
from users.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory
from utils.helpers import create_factory_data


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('word')
    short_description = factory.Faker('word')
    technology = factory.Faker('text')
    start_date = factory.Faker('date_time_between', start_date='-1y', end_date='now')
    end_date = factory.Faker('date_time_between', start_date='-1y', end_date='now')
    currently_working = True if end_date is None else False
    url = factory.Faker('url')
    description = factory.Faker('text')


def create_projects_with_factory(
    num_of_data=7, display_name="project",
    display_name_plural="projects", delete_old_data=False
):

    return create_factory_data(
        factory=ProjectFactory,
        num_of_data=num_of_data,
        display_name=display_name,
        display_name_plural=display_name_plural,
        delete_old_data=delete_old_data,
        model=Project
    )
