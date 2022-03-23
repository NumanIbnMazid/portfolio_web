from django.test import TestCase
from portfolios.models import Interest
from portfolios.factories.interest_factory import create_interests_with_factory


class InterestTestCase(TestCase):
    __MODEL = Interest

    @classmethod
    def setUpTestData(cls):
        # Create dummy interest with Interest factory and assign to class variable
        cls.interest = create_interests_with_factory(num_of_data=1)[0]

    # test if interest is created sucessfully
    def test_interest_created_sucessfully(self):
        instance = self.__MODEL.objects.get(id=self.interest.id)
        self.assertEqual(instance.title, self.interest.title)

    def test_interest_title_label(self):
        field_label = self.interest._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_interest_user_label(self):
        field_label = self.interest._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_interest_title_max_length(self):
        max_length = self.interest._meta.get_field('title').max_length
        self.assertEqual(max_length, 150)

    def test_interest_object_name_is_title(self):
        expected_object_name = f'{self.interest.title}'
        self.assertEqual(expected_object_name, str(self.interest))

    def test_interest_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEqual(self.interest.get_absolute_url(), f'/portfolios/interest/{self.interest.slug}/detail/')
