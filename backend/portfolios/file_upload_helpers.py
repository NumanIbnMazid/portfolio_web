import os
import time
from django.utils.text import slugify
from utils.helpers import get_user_media_path


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def skill_icon_path(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.user)}/skills/{instance.slug[:23]}/{final_filename}"


def professional_experience_company_image_path(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.user)}/professional-experiences/{instance.slug[:23]}/{final_filename}"


def professional_experience_media_path(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.professional_experience.user)}/professional-experiences/{instance.professional_experience.slug[:23]}/media/{final_filename}"


def education_media_path(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.education.user)}/educations/{instance.education.slug[:23]}/media/{final_filename}"


def certification_media_path(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.certification.user)}/certifications/{instance.certification.slug[:23]}/media/{final_filename}"


def project_media_path(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.project.user)}/projects/{instance.project.slug[:23]}/media/{final_filename}"


def interest_icon_path(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.user)}/interests/{instance.slug[:23]}/{final_filename}"


def testimonial_image_path(instance, filename):
    new_filename = "{datetime}".format(datetime=time.strftime("%Y%m%d-%H%M%S"))
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return f"{get_user_media_path(instance.user)}/testimonials/{instance.slug[:23]}/{final_filename}"
