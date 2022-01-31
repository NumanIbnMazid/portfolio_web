import factory
from factory.fuzzy import FuzzyChoice
from portfolios.models import ProfessionalExperience
from users.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory
from utils.helpers import create_factory_data


JOB_TYPES = [JOB_TYPE for JOB_TYPE in ProfessionalExperience.JobType]


class ProfessionalExperienceFactory(DjangoModelFactory):
    class Meta:
        model = ProfessionalExperience

    user = factory.SubFactory(UserFactory)
    company = factory.Faker('word')
    company_image = factory.django.ImageField(color='blue')
    address = factory.Faker('word')
    designation = factory.Faker('word')
    job_type = FuzzyChoice(JOB_TYPES)
    start_date = factory.Faker('date_time_between', start_date='-1y', end_date='now')
    end_date = factory.Faker('date_time_between', start_date='-1y', end_date='now')
    currently_working = True if end_date is None else False
    description = factory.Faker('text')


def create_professional_experiences_with_factory(
    num_of_data=7, display_name="professional-experience",
    display_name_plural="professional-experiences", delete_old_data=False
):

    return create_factory_data(
        factory=ProfessionalExperienceFactory,
        num_of_data=num_of_data,
        display_name=display_name,
        display_name_plural=display_name_plural,
        delete_old_data=delete_old_data,
        model=ProfessionalExperience
    )
