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
