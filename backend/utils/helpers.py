from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
import datetime

def get_user_media_path(user):
    return f"{slugify(user.username[:23])}"

def now():

    """
    Returns an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """

    if settings.USE_TZ:
        return timezone.now()
    else:
        return datetime.now()


def create_factory_data(factory=None, num_of_data=7, display_name="item", display_name_plural="items", delete_old_data=False, model=None):

    """[Creates dummy data]

    Args:
        factory (optional): [Django Factory]. Defaults to None.
        num_of_data (int, optional): [Total number of data to generate]. Defaults to 7.
        display_name (str, optional): [Representational name]. Defaults to "item".
        display_name_plural (str, optional): [Representational name plural]. Defaults to "items".
        delete_old_data (bool, optional): [True, if want to delete old data]. Defaults to False.
        model (optional): [Django Model Class, Required if delete_old_data = True]. Defaults to None.

    Returns:
        [list]: [List of created data]
    """

    if delete_old_data:
        # raise attribute error if model is not provided
        if model is None:
            raise AttributeError(f"{display_name_plural} cannot be deleted without a model. Please provide a model class.")

        # delete old data
        print(f"Deleting old {display_name_plural}...")
        model.objects.all().delete()
        print(f"Deleted old {display_name_plural}...")

    data = []
    print(f"Creating {display_name_plural}...")
    for _ in range(num_of_data):
        instance = factory()
        data.append(instance)
        print(f"Created {display_name}:", instance)
    print(f"Created {display_name_plural}...")

    return data
