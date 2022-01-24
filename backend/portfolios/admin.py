from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import (
    Skill, ProfessionalExperience, ProfessionalExperienceMedia, Education, EducationMedia, Certification, CertificationMedia, Project, ProjectMedia, Interest, Testimonial
)

# ----------------------------------------------------
# *** Skill ***
# ----------------------------------------------------

class SkillAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Skill


admin.site.register(Skill, SkillAdmin)


# ----------------------------------------------------
# *** Professional Experience ***
# ----------------------------------------------------

class ProfessionalExperienceMediaAdmin(admin.StackedInline):
    model = ProfessionalExperienceMedia

class ProfessionalExperienceAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    inlines = [ProfessionalExperienceMediaAdmin]

    class Meta:
        model = ProfessionalExperience


admin.site.register(ProfessionalExperience, ProfessionalExperienceAdmin)


# ----------------------------------------------------
# *** Education ***
# ----------------------------------------------------

class EducationMediaAdmin(admin.StackedInline):
    model = EducationMedia

class EducationAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    inlines = [EducationMediaAdmin]

    class Meta:
        model = Education


admin.site.register(Education, EducationAdmin)


# ----------------------------------------------------
# *** Certification ***
# ----------------------------------------------------

class CertificationMediaAdmin(admin.StackedInline):
    model = CertificationMedia

class CertificationAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    inlines = [CertificationMediaAdmin]

    class Meta:
        model = Certification


admin.site.register(Certification, CertificationAdmin)


# ----------------------------------------------------
# *** Project ***
# ----------------------------------------------------

class ProjectMediaAdmin(admin.StackedInline):
    model = ProjectMedia

class ProjectAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    inlines = [ProjectMediaAdmin]

    class Meta:
        model = Project


admin.site.register(Project, ProjectAdmin)


# ----------------------------------------------------
# *** Interest ***
# ----------------------------------------------------

class InterestAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Interest


admin.site.register(Interest, InterestAdmin)


# ----------------------------------------------------
# *** Testimonial ***
# ----------------------------------------------------

class TestimonialAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Testimonial


admin.site.register(Testimonial, TestimonialAdmin)
