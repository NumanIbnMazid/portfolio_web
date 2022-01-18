from django.shortcuts import render
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

    def get_queryset(self):
        return Skill.objects.all()

    def get_object(self, *args, **kwargs):
        return Skill.objects.get_by_slug(self.kwargs.get('slug'))

    def form_valid(self, form):
        # assign user to the form
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head_title"] = context["page_title"] = "Skills"
        context["form_submit_url"] = 'users:user_profile_update' if getattr(context.get("object", None), "slug", None) else None
        context["form_submit_url_slug"] = getattr(
            context.get("object", None), "slug", None)
        return context
