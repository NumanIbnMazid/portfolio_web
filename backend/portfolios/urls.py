from django.urls import path
from portfolios.views import (
    SkillView,
)

urlpatterns = [
    path("skills/", SkillView.as_view(), name="skills"),
]
