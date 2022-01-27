from django.test import TestCase
from portfolios.models import Skill
from portfolios.factories.skill_factory import create_skills_with_factory

class SkillTestCase(TestCase):
    __MODEL = Skill

    @classmethod
    def setUpTestData(cls):
        # Create dummy skill with Skill factory and assign to class variable
        cls.skill = create_skills_with_factory(num_of_data=1)[0]

    # test if skill is created sucessfully
    def test_skill_create_sucessfully(self):
        instance = self.__MODEL.objects.get(id=self.skill.id)
        self.assertEquals(instance.title, self.skill.title)

    def test_skill_title_label(self):
        field_label = self.skill._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_skill_user_label(self):
        field_label = self.skill._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_skill_title_max_length(self):
        max_length = self.skill._meta.get_field('title').max_length
        self.assertEquals(max_length, 150)

    def test_skill_object_name_is_title(self):
        expected_object_name = f'{self.skill.title}'
        self.assertEquals(expected_object_name, str(self.skill))

    def test_skill_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEquals(self.skill.get_absolute_url(), f'/portfolios/skills/{self.skill.slug}/detail/')
