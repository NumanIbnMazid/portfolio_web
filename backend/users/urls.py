from django.urls import path
from users.views import UserProfileView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("profile/<slug>/update/", UserProfileView.as_view(), name="user_profile_update"),
]
