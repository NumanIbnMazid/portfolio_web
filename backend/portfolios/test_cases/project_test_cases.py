from django.test import TestCase
from portfolios.models import Project
from portfolios.factories.project_factory import create_projects_with_factory


class ProjectTestCase(TestCase):
    __MODEL = Project

    @classmethod
    def setUpTestData(cls):
        # Create dummy project with Project factory and assign to class variable
        cls.project = create_projects_with_factory(num_of_data=1)[0]

    # test if project is created sucessfully
    def test_project_created_sucessfully(self):
        instance = self.__MODEL.objects.get(id=self.project.id)
        self.assertEqual(instance.title, self.project.title)

    def test_project_title_label(self):
        field_label = self.project._meta.get_field('title').verbose_title
        self.assertEqual(field_label, 'title')

    def test_project_user_label(self):
        field_label = self.project._meta.get_field('user').verbose_title
        self.assertEqual(field_label, 'user')

    def test_project_title_max_length(self):
        max_length = self.project._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_project_object_name_is_title(self):
        expected_object_name = f'{self.project.title}'
        self.assertEqual(expected_object_name, str(self.project))

    def test_project_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEqual(
            self.project.get_absolute_url(),
            f'/portfolios/project/{self.project.slug}/detail/'
        )
