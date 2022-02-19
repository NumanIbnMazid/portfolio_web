import factory
from portfolios.models import Education
from users.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory
from utils.helpers import create_factory_data


class EducationFactory(DjangoModelFactory):
    class Meta:
        model = Education

    user = factory.SubFactory(UserFactory)
    school = factory.Faker('word')
    degree = factory.Faker('word')
    address = factory.Faker('word')
    field_of_study = factory.Faker('word')
    start_date = factory.Faker('date_time_between', start_date='-1y', end_date='now')
    end_date = factory.Faker('date_time_between', start_date='-1y', end_date='now')
    currently_studying = True if end_date is None else False
    grade = factory.Faker('word')
    activities = factory.Faker('word')
    description = factory.Faker('text')


def create_educations_with_factory(
    num_of_data=7, display_name="education",
    display_name_plural="educations", delete_old_data=False
):

    return create_factory_data(
        factory=EducationFactory,
        num_of_data=num_of_data,
        display_name=display_name,
        display_name_plural=display_name_plural,
        delete_old_data=delete_old_data,
        model=Education
    )
