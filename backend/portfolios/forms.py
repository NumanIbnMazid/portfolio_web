from django import forms
from portfolios.models import Skill


# ----------------------------------------------------
# *** Skill Forms ***
# ----------------------------------------------------


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('title', 'image')
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'description': forms.TextInput(attrs={'class': 'form-control'}),
        #     'image': forms.FileInput(attrs={'class': 'form-control'}),
        #     'slug': forms.TextInput(attrs={'class': 'form-control'}),
        # }
