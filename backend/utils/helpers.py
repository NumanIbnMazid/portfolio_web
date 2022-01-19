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
