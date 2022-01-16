from django.urls import path
from users.views import UserProfileView, UserProfileUpdateView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("profile/update/<slug>/", UserProfileUpdateView.as_view(), name="user_profile_update"),
]
