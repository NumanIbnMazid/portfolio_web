from django.urls import path
from portfolios.views import (
    SkillView, ProfessionalExperienceView, EducationView
)

urlpatterns = [

    # ----------------------------------------------------
    # *** Skill ***
    # ----------------------------------------------------
    path("skills/", SkillView.as_view(action="list"), name="skills"),
    path("skill/create/", SkillView.as_view(action="create"), name="skill_create"),
    path("skill/<slug>/detail/", SkillView.as_view(action="detail"), name="skill_detail"),
    path("skill/<slug>/update/", SkillView.as_view(action="update"), name="skill_update"),
    path("skill/<slug>/delete/", SkillView.as_view(action="delete"), name="skill_delete"),

    # ----------------------------------------------------
    # *** Professional Experience ***
    # ----------------------------------------------------
    path("professional-experiences/",
         ProfessionalExperienceView.as_view(action="list"), name="professional_experiences"
         ),
    path("professional-experience/create/",
         ProfessionalExperienceView.as_view(action="create"), name="professional_experience_create"
         ),
    path("professional-experience/<slug>/detail/",
         ProfessionalExperienceView.as_view(action="detail"), name="professional_experience_detail"
         ),
    path("professional-experience/<slug>/update/",
         ProfessionalExperienceView.as_view(action="update"), name="professional_experience_update"
         ),
    path("professional-experience/<slug>/delete/",
         ProfessionalExperienceView.as_view(action="delete"), name="professional_experience_delete"
         ),
    # professional experience media
    path("professional-experience-media/<slug>/delete/",
         ProfessionalExperienceView.as_view(action="media_delete"), name="professional_experience_media_delete"
         ),

    # ----------------------------------------------------
    # *** Education ***
    # ----------------------------------------------------
    path("educations/", EducationView.as_view(action="list"), name="educations"),
    path("education/create/", EducationView.as_view(action="create"), name="education_create"),
    path("education/<slug>/detail/", EducationView.as_view(action="detail"), name="education_detail"),
    path("education/<slug>/update/", EducationView.as_view(action="update"), name="education_update"),
    path("education/<slug>/delete/", EducationView.as_view(action="delete"), name="education_delete"),
    # education media
    path("education-media/<slug>/delete/", EducationView.as_view(action="media_delete"), name="education_media_delete"),
]
