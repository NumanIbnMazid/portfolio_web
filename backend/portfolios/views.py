from django import forms
from portfolios.models import Skill, ProfessionalExperience
from portfolios.forms import SkillForm, ProfessionalExperienceForm
from utils.mixins import CustomViewSetMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

skill_decorators = [login_required]



@method_decorator(skill_decorators, name='dispatch')
class SkillView(CustomViewSetMixin):
    template_name = "portfolios/skills/skills.html"
    model = Skill
    form_class = SkillForm
    success_url = 'portfolios:skills'
    lookup_field = 'slug'
    update_success_message = "Skill has been updated successfully."
    url_list = ["skills", "skill_create", "skill_detail", "skill_update", "skill_delete"]

    def get_queryset(self):
        return Skill.objects.all()

    def get_object(self, *args, **kwargs):
        return Skill.objects.get_by_slug(self.kwargs.get('slug'))

    def form_valid(self, form):
        # assign user to the form
        form.instance.user = self.request.user
        # validate unique skill title
        qs = Skill.objects.filter(user=self.request.user, title__iexact=form.cleaned_data.get('title')).exclude(slug__iexact=self.kwargs.get('slug'))
        if qs:
            form.add_error(
                "title", forms.ValidationError(
                    f"This skill already exists!"
                )
            )
        return super().form_valid(form)


class ProfessionalExperienceView(CustomViewSetMixin):
    template_name = "portfolios/professional-experiences/professional-experiences.html"
    snippet_template = "portfolios/professional-experiences/professional-experiences-snippet.html"
    model = ProfessionalExperience
    form_class = ProfessionalExperienceForm
    success_url = 'portfolios:professional_experiences'
    lookup_field = 'slug'
    url_list = ["professional_experiences", "professional_experience_create", "professional_experience_detail", "professional_experience_update", "professional_experience_delete"]

    def get_queryset(self):
        return ProfessionalExperience.objects.all()

    def get_object(self, *args, **kwargs):
        return ProfessionalExperience.objects.get_by_slug(self.kwargs.get('slug'))

    def form_valid(self, form):
        # assign user to the form
        form.instance.user = self.request.user
        # validate unique  company name
        qs = ProfessionalExperience.objects.filter(user=self.request.user, company__iexact=form.cleaned_data.get('company')).exclude(slug__iexact=self.kwargs.get('slug'))
        if qs:
            form.add_error(
                "title", forms.ValidationError(
                    f"This company already exists!"
                )
            )
        return super().form_valid(form)
