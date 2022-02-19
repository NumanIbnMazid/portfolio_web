from django.test import TestCase
from portfolios.models import Education
from portfolios.factories.education_factory import create_educations_with_factory


class EducationTestCase(TestCase):
    __MODEL = Education

    @classmethod
    def setUpTestData(cls):
        # Create dummy education with Education factory and assign to class variable
        cls.education = create_educations_with_factory(num_of_data=1)[0]

    # test if education is created sucessfully
    def test_education_created_sucessfully(self):
        instance = self.__MODEL.objects.get(id=self.education.id)
        self.assertEqual(instance.school, self.education.school)

    def test_education_school_label(self):
        field_label = self.education._meta.get_field('school').verbose_name
        self.assertEqual(field_label, 'school')

    def test_education_user_label(self):
        field_label = self.education._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_education_school_max_length(self):
        max_length = self.education._meta.get_field('school').max_length
        self.assertEqual(max_length, 150)

    def test_education_object_name_is_school(self):
        expected_object_name = f'{self.education.school}'
        self.assertEqual(expected_object_name, str(self.education))

    def test_education_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEqual(
            self.education.get_absolute_url(),
            f'/portfolios/education/{self.education.slug}/detail/'
        )
