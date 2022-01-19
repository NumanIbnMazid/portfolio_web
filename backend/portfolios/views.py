from django import forms
from portfolios.models import Skill
from portfolios.forms import SkillForm
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

    def get_queryset(self):
        return Skill.objects.all()

    def get_object(self, *args, **kwargs):
        return Skill.objects.get_by_slug(self.kwargs.get('slug'))

    def form_valid(self, form):
        # assign user to the form
        form.instance.user = self.request.user
        # validate unique skill title
        qs = Skill.objects.filter(user=self.request.user, title=form.cleaned_data.get('title')).exclude(slug__iexact=self.kwargs.get('slug'))
        if qs:
            form.add_error(
                "title", forms.ValidationError(
                    f"This skill already exists!"
                )
            )
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["display_fields"] = Skill._meta.get_fields()
    #     return context
