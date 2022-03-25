from django import forms
from portfolios.models import (
    Skill,
    ProfessionalExperience, ProfessionalExperienceMedia,
    Education, EducationMedia,
    Certification, CertificationMedia,
    Project, ProjectMedia,
    Interest,
    Testimonial
)
from portfolios.forms import (
    SkillForm,
    ProfessionalExperienceMediaForm, ProfessionalExperienceWithMediaForm,
    EducationWithMediaForm, EducationMediaForm,
    CertificationWithMediaForm, CertificationMediaForm,
    ProjectWithMediaForm, ProjectMediaForm,
    InterestForm,
    TestimonialForm
)
from utils.mixins import CustomViewSetMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.db import transaction
from django.utils.translation import gettext_lazy as _

skill_decorators = professional_experience_decorators = education_decorators = certification_decorators = \
    project_decorators = interest_decorators = testimonial_decorators = [login_required]


# ----------------------------------------------------
# *** Skill ***
# ----------------------------------------------------

@method_decorator(skill_decorators, name='dispatch')
class SkillView(CustomViewSetMixin):
    template_name = "portfolios/skills/skills.html"
    model = Skill
    form_class = SkillForm
    success_url = 'portfolios:skills'
    lookup_field = 'slug'
    update_success_message = _("Skill has been updated successfully.")
    url_list = ["skills", "skill_create", "skill_detail", "skill_update", "skill_delete"]

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return Skill.objects.get_by_slug(self.kwargs.get('slug'))

    def form_valid(self, form):
        # assign user to the form
        form.instance.user = self.request.user
        # validate unique skill title
        qs = Skill.objects.filter(user=self.request.user, title__iexact=form.cleaned_data.get('title')).\
            exclude(slug__iexact=self.kwargs.get('slug'))
        if qs:
            form.add_error(
                "title", forms.ValidationError(
                    _("This skill already exists!")
                )
            )
        return super().form_valid(form)


# ----------------------------------------------------
# *** Professional Experience ***
# ----------------------------------------------------

@method_decorator(professional_experience_decorators, name='dispatch')
class ProfessionalExperienceView(CustomViewSetMixin):
    template_name = "portfolios/professional-experiences/professional-experiences.html"
    snippet_template = "portfolios/professional-experiences/professional-experiences-snippet.html"
    model = ProfessionalExperience
    form_class = ProfessionalExperienceWithMediaForm
    paginate_by = 4
    success_url = 'portfolios:professional_experiences'
    lookup_field = 'slug'
    url_list = [
        "professional_experiences", "professional_experience_create", "professional_experience_detail",
        "professional_experience_update", "professional_experience_delete"
    ]

    def get_queryset(self):
        return ProfessionalExperience.objects.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return ProfessionalExperience.objects.get_by_slug(self.kwargs.get('slug'))

    def get_media_delete_context_data(self, **kwargs):
        context = {}
        context["page_title"] = context["head_title"] = _("Delete Professional Experience Media")
        context["action"] = "delete"
        return context

    def media_delete(self, request, *args, **kwargs):
        qs = ProfessionalExperienceMedia.objects.filter(slug=self.kwargs.get('slug'))
        if qs:
            # delete object
            qs.delete()
            # add success message
            messages.add_message(
                self.request, messages.SUCCESS, _("Media Deleted Successfully!")
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                self.request, messages.ERROR, _("Media not found!")
            )
            raise Http404(_("Object not found!"))

    def form_valid(self, form):
        if form.is_valid():

            # assign user to the form
            form.instance.user = self.request.user

            # validate unique  company name
            qs = ProfessionalExperience.objects.filter(
                user=self.request.user, company__iexact=form.cleaned_data.get('company')
            ).exclude(slug__iexact=self.kwargs.get('slug'))

            if qs:
                form.add_error(
                    "title", forms.ValidationError(
                        _("This company already exists!")
                    )
                )
                return super().form_invalid(form)

            # save the form
            self.object = form.save()

            # get files from form
            files = self.request.FILES.getlist('file')

            # save professional experience media files to the database if any
            professional_experience_media_form = ProfessionalExperienceMediaForm(self.request.POST, self.request.FILES)
            # check if the form is valid and form has files
            if professional_experience_media_form.is_valid() and len(files) >= 1:
                with transaction.atomic():  # ensure that all objects are saved otherwise rollback
                    for file in files:
                        ProfessionalExperienceMedia.objects.update_or_create(
                            professional_experience=self.object,
                            file=file
                        )

            return super().form_valid(form)
        return super().form_invalid(form)


# ----------------------------------------------------
# *** Education ***
# ----------------------------------------------------


@method_decorator(education_decorators, name='dispatch')
class EducationView(CustomViewSetMixin):
    template_name = "portfolios/educations/educations.html"
    snippet_template = "portfolios/educations/educations-snippet.html"
    model = Education
    form_class = EducationWithMediaForm
    paginate_by = 4
    success_url = 'portfolios:educations'
    lookup_field = 'slug'
    display_fields = [
        'school', 'degree', 'address', 'field_of_study', 'start_date', 'end_date', 'currently_studying', 'grade',
        'activities', 'description'
    ]
    url_list = [
        "educations", "education_create", "education_detail", "education_update", "education_delete"
    ]

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return Education.objects.get_by_slug(self.kwargs.get('slug'))

    def get_media_delete_context_data(self, **kwargs):
        context = {}
        context["page_title"] = context["head_title"] = _("Delete Education Media")
        context["action"] = "delete"
        return context

    def media_delete(self, request, *args, **kwargs):
        qs = EducationMedia.objects.filter(slug=self.kwargs.get('slug'))
        if qs:
            # delete object
            qs.delete()
            # add success message
            messages.add_message(
                self.request, messages.SUCCESS, _("Media Deleted Successfully!")
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                self.request, messages.ERROR, _("Media not found!")
            )
            raise Http404(_("Object not found!"))

    def form_valid(self, form):
        if form.is_valid():

            # assign user to the form
            form.instance.user = self.request.user

            # validate unique school name
            qs = Education.objects.filter(
                user=self.request.user, school__iexact=form.cleaned_data.get('school')
            ).exclude(slug__iexact=self.kwargs.get('slug'))

            if qs:
                form.add_error(
                    "title", forms.ValidationError(
                        _("This school already exists!")
                    )
                )
                return super().form_invalid(form)

            # save the form
            self.object = form.save()

            # get files from form
            files = self.request.FILES.getlist('file')

            # save Education media files to the database if any
            education_media_form = EducationMediaForm(self.request.POST, self.request.FILES)
            # check if the form is valid and form has files
            if education_media_form.is_valid() and len(files) >= 1:
                with transaction.atomic():  # ensure that all objects are saved otherwise rollback
                    for file in files:
                        EducationMedia.objects.update_or_create(
                            education=self.object,
                            file=file
                        )

            return super().form_valid(form)
        return super().form_invalid(form)


# ----------------------------------------------------
# *** Certification ***
# ----------------------------------------------------


@method_decorator(certification_decorators, name='dispatch')
class CertificationView(CustomViewSetMixin):
    template_name = "portfolios/certifications/certifications.html"
    snippet_template = "portfolios/certifications/certifications-snippet.html"
    model = Certification
    form_class = CertificationWithMediaForm
    paginate_by = 4
    success_url = 'portfolios:certifications'
    lookup_field = 'slug'
    display_fields = [
        'name', 'organization', 'address', 'issue_date', 'expiration_date', 'does_not_expire', 'credential_id',
        'credential_url', 'description'
    ]
    url_list = [
        "certifications", "certification_create", "certification_detail", "certification_update", "certification_delete"
    ]

    def get_queryset(self):
        return Certification.objects.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return Certification.objects.get_by_slug(self.kwargs.get('slug'))

    def get_media_delete_context_data(self, **kwargs):
        context = {}
        context["page_title"] = context["head_title"] = _("Delete Certification Media")
        context["action"] = "delete"
        return context

    def media_delete(self, request, *args, **kwargs):
        qs = CertificationMedia.objects.filter(slug=self.kwargs.get('slug'))
        if qs:
            # delete object
            qs.delete()
            # add success message
            messages.add_message(
                self.request, messages.SUCCESS, _("Media Deleted Successfully!")
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                self.request, messages.ERROR, _("Media not found!")
            )
            raise Http404(_("Object not found!"))

    def form_valid(self, form):
        if form.is_valid():

            # assign user to the form
            form.instance.user = self.request.user

            # validate unique name
            qs = Certification.objects.filter(
                user=self.request.user, name__iexact=form.cleaned_data.get('name')
            ).exclude(slug__iexact=self.kwargs.get('slug'))

            if qs:
                form.add_error(
                    "title", forms.ValidationError(
                        _("This certification already exists!")
                    )
                )
                return super().form_invalid(form)

            # save the form
            self.object = form.save()

            # get files from form
            files = self.request.FILES.getlist('file')

            # save Certification media files to the database if any
            certification_media_form = CertificationMediaForm(self.request.POST, self.request.FILES)
            # check if the form is valid and form has files
            if certification_media_form.is_valid() and len(files) >= 1:
                with transaction.atomic():  # ensure that all objects are saved otherwise rollback
                    for file in files:
                        CertificationMedia.objects.update_or_create(
                            certification=self.object,
                            file=file
                        )

            return super().form_valid(form)
        return super().form_invalid(form)


# ----------------------------------------------------
# *** Project ***
# ----------------------------------------------------


@method_decorator(project_decorators, name='dispatch')
class ProjectView(CustomViewSetMixin):
    template_name = "portfolios/projects/projects.html"
    snippet_template = "portfolios/projects/projects-snippet.html"
    model = Project
    form_class = ProjectWithMediaForm
    paginate_by = 4
    success_url = 'portfolios:projects'
    lookup_field = 'slug'
    display_fields = [
        'title', 'short_description', 'technology', 'start_date', 'end_date', 'currently_working', 'url',
        'description'
    ]
    url_list = [
        "projects", "project_create", "project_detail", "project_update", "project_delete"
    ]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return Project.objects.get_by_slug(self.kwargs.get('slug'))

    def get_media_delete_context_data(self, **kwargs):
        context = {}
        context["page_title"] = context["head_title"] = _("Delete Project Media")
        context["action"] = "delete"
        return context

    def media_delete(self, request, *args, **kwargs):
        qs = ProjectMedia.objects.filter(slug=self.kwargs.get('slug'))
        if qs:
            # delete object
            qs.delete()
            # add success message
            messages.add_message(
                self.request, messages.SUCCESS, _("Media Deleted Successfully!")
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                self.request, messages.ERROR, _("Media not found!")
            )
            raise Http404(_("Object not found!"))

    def form_valid(self, form):
        if form.is_valid():

            # assign user to the form
            form.instance.user = self.request.user

            # validate unique title
            qs = Project.objects.filter(
                user=self.request.user, title__iexact=form.cleaned_data.get('title')
            ).exclude(slug__iexact=self.kwargs.get('slug'))

            if qs:
                form.add_error(
                    "title", forms.ValidationError(
                        _("This project already exists!")
                    )
                )
                return super().form_invalid(form)

            # save the form
            self.object = form.save()

            # get files from form
            files = self.request.FILES.getlist('file')

            # save Project media files to the database if any
            project_media_form = ProjectMediaForm(self.request.POST, self.request.FILES)
            # check if the form is valid and form has files
            if project_media_form.is_valid() and len(files) >= 1:
                with transaction.atomic():  # ensure that all objects are saved otherwise rollback
                    for file in files:
                        ProjectMedia.objects.update_or_create(
                            project=self.object,
                            file=file
                        )

            return super().form_valid(form)
        return super().form_invalid(form)


# ----------------------------------------------------
# *** Interest ***
# ----------------------------------------------------

@method_decorator(interest_decorators, name='dispatch')
class InterestView(CustomViewSetMixin):
    template_name = "portfolios/interests/interests.html"
    model = Interest
    form_class = InterestForm
    success_url = 'portfolios:interests'
    lookup_field = 'slug'
    update_success_message = _("Interest has been updated successfully.")
    url_list = ["interests", "interest_create", "interest_detail", "interest_update", "interest_delete"]

    def get_queryset(self):
        return Interest.objects.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return Interest.objects.get_by_slug(self.kwargs.get('slug'))

    def form_valid(self, form):
        # assign user to the form
        form.instance.user = self.request.user
        # validate unique interest title
        qs = Interest.objects.filter(user=self.request.user, title__iexact=form.cleaned_data.get('title')).\
            exclude(slug__iexact=self.kwargs.get('slug'))
        if qs:
            form.add_error(
                "title", forms.ValidationError(
                    _("This interest already exists!")
                )
            )
        return super().form_valid(form)


# ----------------------------------------------------
# *** Testimonial ***
# ----------------------------------------------------

@method_decorator(testimonial_decorators, name='dispatch')
class TestimonialView(CustomViewSetMixin):
    template_name = "portfolios/testimonials/testimonials.html"
    model = Testimonial
    form_class = TestimonialForm
    success_url = 'portfolios:testimonials'
    lookup_field = 'slug'
    update_success_message = _("Testimonial has been updated successfully.")
    url_list = ["testimonials", "testimonial_create", "testimonial_detail", "testimonial_update", "testimonial_delete"]

    def get_queryset(self):
        return Testimonial.objects.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return Testimonial.objects.get_by_slug(self.kwargs.get('slug'))

    def form_valid(self, form):
        # assign user to the form
        form.instance.user = self.request.user
        # validate unique testimonial name
        qs = Testimonial.objects.filter(user=self.request.user, name__iexact=form.cleaned_data.get('name')).\
            exclude(slug__iexact=self.kwargs.get('slug'))
        if qs:
            form.add_error(
                "name", forms.ValidationError(
                    _("This testimonial already exists!")
                )
            )
        return super().form_valid(form)
