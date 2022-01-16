import os
import time
from django.utils.text import slugify
from utils.helpers import get_user_media_path


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_skill_icon(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.user)}/skills/{slugify(instance.title[:100])}/{final_filename}"

def upload_professional_experience_media(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.professional_experience.user)}/professional-experiences/{slugify(instance.professional_experience.__str__()[:100])}/media/{final_filename}"


def upload_education_media(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.education.user)}/educations/{slugify(instance.education.__str__()[:100])}/media/{final_filename}"


def upload_certification_media(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.certification.user)}/certifications/{slugify(instance.certification.__str__()[:100])}/media/{final_filename}"


def upload_project_media(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.project.user)}/projects/{slugify(instance.project.__str__()[:100])}/media/{final_filename}"


def upload_interest_icon(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.user)}/interests/{slugify(instance.title[:100])}/{final_filename}"


def upload_testimonial_image(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.user)}/testimonials/{slugify(instance.overview[:100])}/{final_filename}"
