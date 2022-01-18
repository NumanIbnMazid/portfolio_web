from django.urls import path
from portfolios.views import (
    SkillView,
)

urlpatterns = [
    path("skills/", SkillView.as_view(action="list"), name="skills"),
    path("skills/create/", SkillView.as_view(action="create"), name="skill_create"),
    path("skills/<slug>/update/", SkillView.as_view(action="update"), name="skill_update"),
]
