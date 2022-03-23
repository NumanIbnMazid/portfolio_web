from django.test import TestCase
from portfolios.models import Certification
from portfolios.factories.certification_factory import create_certifications_with_factory


class CertificationTestCase(TestCase):
    __MODEL = Certification

    @classmethod
    def setUpTestData(cls):
        # Create dummy certification with Certification factory and assign to class variable
        cls.certification = create_certifications_with_factory(num_of_data=1)[0]

    # test if certification is created sucessfully
    def test_certification_created_sucessfully(self):
        instance = self.__MODEL.objects.get(id=self.certification.id)
        self.assertEqual(instance.name, self.certification.name)

    def test_certification_name_label(self):
        field_label = self.certification._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_certification_user_label(self):
        field_label = self.certification._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_certification_name_max_length(self):
        max_length = self.certification._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

    def test_certification_object_name_is_name(self):
        expected_object_name = f'{self.certification.name}'
        self.assertEqual(expected_object_name, str(self.certification))

    def test_certification_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEqual(
            self.certification.get_absolute_url(),
            f'/portfolios/certification/{self.certification.slug}/detail/'
        )
