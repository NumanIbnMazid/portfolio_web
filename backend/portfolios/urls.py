from django.urls import path
from portfolios.views import (
    SkillView,
)

urlpatterns = [
    path("skills/", SkillView.as_view(action="list"), name="skills"),
    path("skills/create/", SkillView.as_view(action="create"), name="skill_create"),
    path("skills/<slug>/detail/", SkillView.as_view(action="detail"), name="skill_detail"),
    path("skills/<slug>/update/", SkillView.as_view(action="update"), name="skill_update"),
    path("skills/<slug>/delete/", SkillView.as_view(action="delete"), name="skill_delete"),
]
