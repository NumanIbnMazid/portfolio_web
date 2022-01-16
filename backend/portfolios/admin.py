from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import (
    Skill, ProfessionalExperience, ProfessionalExperienceMedia, Education, EducationMedia, Certification, CertificationMedia, Project, ProjectMedia, Interest, Testimonial
)


class SkillAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Skill


admin.site.register(Skill, SkillAdmin)


class ProfessionalExperienceAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = ProfessionalExperience


admin.site.register(ProfessionalExperience, ProfessionalExperienceAdmin)


class ProfessionalExperienceMediaAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = ProfessionalExperienceMedia


admin.site.register(ProfessionalExperienceMedia, ProfessionalExperienceMediaAdmin)


class EducationAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Education


admin.site.register(Education, EducationAdmin)


class EducationMediaAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = EducationMedia


admin.site.register(EducationMedia, EducationMediaAdmin)


class CertificationAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Certification


admin.site.register(Certification, CertificationAdmin)


class CertificationMediaAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = CertificationMedia


admin.site.register(CertificationMedia, CertificationMediaAdmin)


class ProjectAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Project


admin.site.register(Project, ProjectAdmin)


class ProjectMediaAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = ProjectMedia


admin.site.register(ProjectMedia, ProjectMediaAdmin)


class InterestAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Interest


admin.site.register(Interest, InterestAdmin)


class TestimonialAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Testimonial


admin.site.register(Testimonial, TestimonialAdmin)
