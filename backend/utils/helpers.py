from django.utils.text import slugify

def get_user_media_path(user):
    return f"{slugify(user.username[:50])}"
