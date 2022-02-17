from django.test import TestCase
from portfolios.models import ProfessionalExperience
from portfolios.factories.professional_experience_factory import create_professional_experiences_with_factory


class ProfessionalExperienceTestCase(TestCase):
    __MODEL = ProfessionalExperience

    @classmethod
    def setUpTestData(cls):
        # Create dummy professional experience with ProfessionalExperience factory and assign to class variable
        cls.professional_experience = create_professional_experiences_with_factory(num_of_data=1)[0]

    # test if professional experience is created sucessfully
    def test_professional_experience_created_sucessfully(self):
        instance = self.__MODEL.objects.get(id=self.professional_experience.id)
        self.assertEqual(instance.company, self.professional_experience.company)

    def test_professional_experience_company_label(self):
        field_label = self.professional_experience._meta.get_field('company').verbose_name
        self.assertEqual(field_label, 'company')

    def test_professional_experience_user_label(self):
        field_label = self.professional_experience._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_professional_experience_company_max_length(self):
        max_length = self.professional_experience._meta.get_field('company').max_length
        self.assertEqual(max_length, 150)

    def test_professional_experience_object_name_is_company(self):
        expected_object_name = f'{self.professional_experience.company}'
        self.assertEqual(expected_object_name, str(self.professional_experience))

    def test_professional_experience_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEqual(
            self.professional_experience.get_absolute_url(),
            f'/portfolios/professional-experience/{self.professional_experience.slug}/detail/'
        )
