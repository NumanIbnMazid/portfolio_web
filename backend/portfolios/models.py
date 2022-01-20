from django.db import models
from django.http import Http404
from django.contrib.auth import get_user_model
from utils.snippets import autoslugFromUUID, autoslugWithFieldAndUUID
from django.utils.translation import gettext_lazy as _
from portfolios.file_upload_helpers import (
    skill_icon_path, professional_experience_media_path, education_media_path, certification_media_path, project_media_path, interest_icon_path, testimonial_image_path
)


""" *************** Skill *************** """

class SkillManager(models.Manager):

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        try:
            instance = self.get_queryset().get(id=id)
        except Skill.DoesNotExist:
            raise Http404("Not Found !!!")
        except Skill.MultipleObjectsReturned:
            qs = self.get_queryset().filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def get_by_slug(self, slug):
        try:
            instance = self.get_queryset().get(slug=slug)
        except Skill.DoesNotExist:
            raise Http404("Not Found !!!")
        except Skill.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

@autoslugWithFieldAndUUID(fieldname="title")
class Skill(models.Model):
    """
    Skill model.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_skills")
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=skill_icon_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # custom model manager
    objects = SkillManager()

    class Meta:
        db_table = 'skill'
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ['-created_at']
        get_latest_by = "created_at"
        unique_together = (('user', 'title'),)

    def __str__(self):
        return self.title

    def unique_error_message(self, model_class, unique_check):
        """ custom `unique_error_message` for `unique_together` validation """
        # custom error message map
        unique_error_message_map = {
            ('user', 'title',): f"{model_class.__name__} `{self.title}` already exists.",
        }
        # get custom error message from map
        if unique_check in unique_error_message_map:
            return unique_error_message_map[unique_check]
        # default error message
        return super().unique_error_message(model_class, unique_check)


""" *************** Professional Experience *************** """


class ProfessionalExperienceManager(models.Manager):

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        try:
            instance = self.get_queryset().get(id=id)
        except ProfessionalExperience.DoesNotExist:
            raise Http404("Not Found !!!")
        except ProfessionalExperience.MultipleObjectsReturned:
            qs = self.get_queryset().filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance

    def get_by_slug(self, slug):
        try:
            instance = self.get_queryset().get(slug=slug)
        except ProfessionalExperience.DoesNotExist:
            raise Http404("Not Found !!!")
        except ProfessionalExperience.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong !!!")
        return instance


@autoslugWithFieldAndUUID(fieldname="company")
class ProfessionalExperience(models.Model):
    """
    Professional Experience model.
    Details: Includes Job Experiences and other professional experiences.
    """
    class JobType(models.TextChoices):
        FULL_TIME = 'Full Time', _('Full Time')
        PART_TIME = 'Part Time', _('Part Time')
        CONTRACTUAL = 'Contractual', _('Contractual')
        REMOTE = 'Remote', _('Remote')

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_professional_experiences")
    slug = models.SlugField(max_length=255, unique=True)
    company = models.CharField(max_length=150)
    address = models.CharField(max_length=254)
    designation = models.CharField(max_length=150)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # custom model manager
    objects = ProfessionalExperienceManager()

    class Meta:
        db_table = 'professional_experience'
        verbose_name = 'Professional Experience'
        verbose_name_plural = 'Professional Experiences'
        ordering = ['-created_at']
        get_latest_by = "created_at"

    def __str__(self):
        return self.company

    def get_end_date(self):
        if self.currently_working:
            return _('Present')
        elif self.end_date:
            return self.end_date.strftime("%B %Y")
        return _('Not Specified')

@autoslugFromUUID()
class ProfessionalExperienceMedia(models.Model):
    professional_experience = models.ForeignKey(ProfessionalExperience, on_delete=models.CASCADE, related_name="professional_experience_media")
    slug = models.SlugField(max_length=255, unique=True)
    file = models.FileField(upload_to=professional_experience_media_path)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'professional_experience_media'
        verbose_name = 'Professional Experience Media'
        verbose_name_plural = 'Professional Experience Media'
        get_latest_by = "created_at"
        order_with_respect_to = 'professional_experience'

    def __str__(self):
        return self.professional_experience.__str__()


""" *************** Education *************** """


@autoslugWithFieldAndUUID(fieldname="school")
class Education(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_educations")
    slug = models.SlugField(max_length=255, unique=True)
    degree = models.CharField(max_length=150)
    school = models.CharField(max_length=150)
    address = models.CharField(max_length=254)
    field_of_study = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_studying = models.BooleanField(default=False)
    grade = models.CharField(max_length=254, blank=True, null=True)
    activities = models.CharField(max_length=254, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'education'
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'
        ordering = ['-created_at']
        get_latest_by = "created_at"

    def __str__(self):
        return self.degree

    def get_end_date(self):
        if self.currently_studying:
            return _('Present')
        elif self.end_date:
            return self.end_date.strftime("%B %Y")
        return _('Not Specified')


@autoslugFromUUID()
class EducationMedia(models.Model):
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name="education_media")
    slug = models.SlugField(max_length=255, unique=True)
    file = models.FileField(upload_to=education_media_path)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'education_media'
        verbose_name = 'Education Media'
        verbose_name_plural = 'Education Media'
        get_latest_by = "created_at"
        order_with_respect_to = 'education'

    def __str__(self):
        return self.education.__str__()


""" *************** Certification *************** """


@autoslugWithFieldAndUUID(fieldname="organization")
class Certification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_certifications")
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    address = models.CharField(max_length=254)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    does_not_expire = models.BooleanField(default=False)
    credential_id = models.CharField(max_length=254, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'certification'
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
        ordering = ['-created_at']
        get_latest_by = "created_at"

    def __str__(self):
        return self.name


@autoslugFromUUID()
class CertificationMedia(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name="certification_media")
    slug = models.SlugField(max_length=255, unique=True)
    file = models.FileField(upload_to=certification_media_path)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'certification_media'
        verbose_name = 'Certification Media'
        verbose_name_plural = 'Certification Media'
        get_latest_by = "created_at"
        order_with_respect_to = 'certification'

    def __str__(self):
        return self.certification.__str__()


""" *************** Project *************** """


@autoslugWithFieldAndUUID(fieldname="title")
class Project(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_projects")
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=254)
    technology = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']
        get_latest_by = "created_at"

    def __str__(self):
        return self.title


@autoslugFromUUID()
class ProjectMedia(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_media")
    slug = models.SlugField(max_length=255, unique=True)
    file = models.FileField(upload_to=project_media_path)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_media'
        verbose_name = 'Project Media'
        verbose_name_plural = 'Project Media'
        get_latest_by = "created_at"
        order_with_respect_to = 'project'

    def __str__(self):
        return self.project.__str__()


""" *************** Interest *************** """


@autoslugWithFieldAndUUID(fieldname="title")
class Interest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_interests")
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=200)
    icon = models.ImageField(upload_to=interest_icon_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interest'
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'
        ordering = ['-created_at']
        get_latest_by = "created_at"

    def __str__(self):
        return self.title


""" *************** Testimonial *************** """


@autoslugFromUUID()
class Testimonial(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_testimonials")
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    image = models.ImageField(upload_to=testimonial_image_path, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'testimonial'
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-created_at']
        get_latest_by = "created_at"

    def __str__(self):
        return self.name
