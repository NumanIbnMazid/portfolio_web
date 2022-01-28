from django.test import TestCase
from django.contrib.auth import get_user_model
from users.factories.user_factory import create_users_with_factory


class UserTestCase(TestCase):
    __MODEL = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.user = create_users_with_factory(num_of_data=1)[0]

    # test if data is created sucessfully
    def test_data_created_sucessfully(self):
        instance = self.__MODEL.objects.get(id=self.user.id)
        self.assertEqual(instance.username, self.user.username)
