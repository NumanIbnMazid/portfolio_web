import factory
from portfolios.models import Testimonial
from users.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory
from utils.helpers import create_factory_data


class TestimonialFactory(DjangoModelFactory):
    class Meta:
        model = Testimonial

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    designation = factory.Faker('word')
    image = factory.django.ImageField(color='blue')
    description = factory.Faker('text')


def create_testimonials_with_factory(
    num_of_data=7, display_name="testimonial",
    display_name_plural="testimonials", delete_old_data=False
):

    return create_factory_data(
        factory=TestimonialFactory,
        num_of_data=num_of_data,
        display_name=display_name,
        display_name_plural=display_name_plural,
        delete_old_data=delete_old_data,
        model=Testimonial
    )
