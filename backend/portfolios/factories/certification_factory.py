import factory
from portfolios.models import Certification
from users.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory
from utils.helpers import create_factory_data


class CertificationFactory(DjangoModelFactory):
    class Meta:
        model = Certification

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    organization = factory.Faker('word')
    address = factory.Faker('word')
    issue_date = factory.Faker('date_time_between', issue_date='-1y', expiration_date='now')
    expiration_date = factory.Faker('date_time_between', issue_date='-1y', expiration_date='now')
    does_not_expire = True if expiration_date is None else False
    credential_id = factory.Faker('number')
    credential_url = factory.Faker('url')
    description = factory.Faker('text')


def create_certifications_with_factory(
    num_of_data=7, display_name="certification",
    display_name_plural="certifications", delete_old_data=False
):

    return create_factory_data(
        factory=CertificationFactory,
        num_of_data=num_of_data,
        display_name=display_name,
        display_name_plural=display_name_plural,
        delete_old_data=delete_old_data,
        model=Certification
    )
