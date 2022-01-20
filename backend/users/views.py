from django.contrib.auth import get_user_model
from users.forms import UserProfileForm
from utils.mixins import CustomViewSetMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

user_profile_decorators = [login_required]

@method_decorator(user_profile_decorators, name='dispatch')
class UserProfileView(CustomViewSetMixin):
    template_name = "users/profile.html"
    snippet_template = "users/profile-snippet.html"
    model = get_user_model()
    form_class = UserProfileForm
    success_url = 'users:user_profile'
    success_message = "Profile updated successfully"

    def get_object(self):
        return get_user_model().objects.get_by_slug(self.request.user.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head_title"] = context["page_title"] = "User Profile Update"
        return context

# @method_decorator(user_profile_decorators, name='dispatch')
# class UserProfileView(View, ContextMixinView):

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return render(request, "users/profile.html", context=context)

#     def get_user_profile(self):
#         qs = get_user_model().objects.filter(slug__iexact=self.request.user.slug)
#         if qs:
#             return qs.first()
#         return None

#     def get_additional_context_data(self, **kwargs):
#         context = {}
#         context["object"] = self.get_user_profile()
#         context["head_title"] = context["page_title"] = "User Profile"
#         context["form"] = UserProfileForm(instance=context.get("object", None))
#         context["form_submit_url"] = 'users:user_profile_update'
#         context["form_submit_url_slug"] = getattr(context.get("object", None), "slug", None)
#         return context
