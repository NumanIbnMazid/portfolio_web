from django.test import TestCase
from portfolios.models import Testimonial
from portfolios.factories.testimonial_factory import create_testimonials_with_factory


class TestimonialTestCase(TestCase):
    __MODEL = Testimonial

    @classmethod
    def setUpTestData(cls):
        # Create dummy testimonial with Testimonial factory and assign to class variable
        cls.testimonial = create_testimonials_with_factory(num_of_data=1)[0]

    # test if testimonial is created sucessfully
    def test_testimonial_created_sucessfully(self):
        instance = self.__MODEL.objects.get(id=self.testimonial.id)
        self.assertEqual(instance.name, self.testimonial.name)

    def test_testimonial_name_label(self):
        field_label = self.testimonial._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_testimonial_user_label(self):
        field_label = self.testimonial._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_testimonial_name_max_length(self):
        max_length = self.testimonial._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

    def test_testimonial_object_name_is_name(self):
        expected_object_name = f'{self.testimonial.name}'
        self.assertEqual(expected_object_name, str(self.testimonial))

    def test_testimonial_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEqual(self.testimonial.get_absolute_url(),
                         f'/portfolios/testimonial/{self.testimonial.slug}/detail/'
                         )
