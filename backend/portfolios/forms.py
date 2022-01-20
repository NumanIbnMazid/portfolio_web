from django import forms
from portfolios.models import Skill, ProfessionalExperience


# ----------------------------------------------------
# *** Skill Forms ***
# ----------------------------------------------------


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('title', 'image')

class ProfessionalExperienceForm(forms.ModelForm):
    class Meta:
        model = ProfessionalExperience
        fields = ('company', 'address', 'designation', 'job_type', 'start_date', 'end_date', 'currently_working', 'description')
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'start_date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'end_date'}),
        }
