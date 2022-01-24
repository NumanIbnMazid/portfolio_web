from django import forms
from portfolios.models import Skill, ProfessionalExperience, ProfessionalExperienceMedia
from utils.validators import get_validated_file, get_validated_image


# ----------------------------------------------------
# *** Skill Forms ***
# ----------------------------------------------------


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('title', 'image')

    def clean_image(self):
        image = self.cleaned_data.get('image')
        return get_validated_image(image)


# ----------------------------------------------------
# *** Professional Experience Forms ***
# ----------------------------------------------------

class ProfessionalExperienceForm(forms.ModelForm):
    class Meta:
        model = ProfessionalExperience
        fields = ['company', 'company_image', 'address', 'designation', 'job_type',
                  'start_date', 'end_date', 'currently_working', 'description']
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

    def clean(self):
        if self.cleaned_data.get('end_date', None) is None and not self.cleaned_data.get('currently_working', None):
            self.add_error('end_date', "End date is required if you are not currently working here.")
        elif self.cleaned_data.get('end_date') is not None and self.cleaned_data.get('currently_working'):
            self.add_error('end_date', "End date is not required if you are currently working here.")
            self.add_error('currently_working', "Currently working is not required if you provide an end date.")
            raise forms.ValidationError("Conflicting with `End date` and `Currently working`. Please specify only one.")
        return self.cleaned_data

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date and end_date <= self.cleaned_data.get('start_date'):
            raise forms.ValidationError("End date must be greater than start date")
        return end_date

    def clean_company_image(self):
        company_image = self.cleaned_data.get('company_image')
        return get_validated_image(company_image)

class ProfessionalExperienceMediaForm(forms.ModelForm):
    class Meta:
        model = ProfessionalExperienceMedia
        fields = ("file",)

class ProfessionalExperienceWithMediaForm(ProfessionalExperienceForm):
    """ ProfessionalExperienceWithMediaForm = ProfessionalExperienceForm + ProfessionalExperienceMediaForm """

    # multiple file form field
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(ProfessionalExperienceForm.Meta):
        fields = ProfessionalExperienceForm.Meta.fields + ['file',]

    def clean_file(self):
        file = self.cleaned_data.get('file')
        return get_validated_file(file)
