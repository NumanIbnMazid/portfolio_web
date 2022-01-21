from django import forms
from portfolios.models import Skill, ProfessionalExperience
from django.conf import settings
import os
from django.core.files.uploadedfile import UploadedFile
from django.template.defaultfilters import filesizeformat


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
        fields = ('company', 'company_image', 'address', 'designation', 'job_type',
                  'start_date', 'end_date', 'currently_working', 'description')
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'start_date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'end_date'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'cols': 3,
                }
            ),
        }

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date and end_date <= self.cleaned_data.get('start_date'):
            raise forms.ValidationError("End date must be greater than start date")
        return end_date

    def clean_company_image(self):
        company_image = self.cleaned_data.get('company_image')
        if company_image and isinstance(company_image, UploadedFile):
            file_extension = os.path.splitext(company_image.name)[1]
            allowed_image_types = settings.ALLOWED_IMAGE_TYPES
            if not file_extension in allowed_image_types:
                raise forms.ValidationError("Only %s file formats are supported! Current image format is %s" % (
                    allowed_image_types, file_extension))
            if company_image.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(company_image.size)))
        return company_image
