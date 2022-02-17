from django import forms
from portfolios.models import (
    Skill,
    ProfessionalExperience, ProfessionalExperienceMedia,
    Education, EducationMedia,
)
from portfolios.forms import (
    SkillForm,
    ProfessionalExperienceMediaForm, ProfessionalExperienceWithMediaForm,
    EducationWithMediaForm, EducationMediaForm,
)
from utils.mixins import CustomViewSetMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.db import transaction
from django.utils.translation import gettext_lazy as _

skill_decorators = professional_experience_decorators = education_decorators = [login_required]


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
        return Skill.objects.all()

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
        return ProfessionalExperience.objects.all()

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
    # template_name = "portfolios/educations/educations.html"
    template_name = "snippets/list-common.html"
    snippet_template = "portfolios/educations/educations-snippet.html"
    model = Education
    form_class = EducationWithMediaForm
    paginate_by = 4
    success_url = 'portfolios:educations'
    lookup_field = 'slug'
    url_list = [
        "educations", "education_create", "education_detail",
        "education_update", "education_delete"
    ]

    def get_queryset(self):
        return Education.objects.all()

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
