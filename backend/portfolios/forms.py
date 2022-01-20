from django import forms
from portfolios.models import Skill
from django.core.exceptions import NON_FIELD_ERRORS


# ----------------------------------------------------
# *** Skill Forms ***
# ----------------------------------------------------


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('title', 'image')
        # widgets = {
            # 'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'description': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control'}),
            # 'slug': forms.TextInput(attrs={'class': 'form-control'}),
        # }
