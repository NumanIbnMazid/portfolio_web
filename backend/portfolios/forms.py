from django import forms
from django.utils.translation import gettext_lazy as _
from portfolios.models import (
    Skill,
    ProfessionalExperience, ProfessionalExperienceMedia,
    Education, EducationMedia,
    Certification, CertificationMedia,
    Project, ProjectMedia,
    Interest,
    Testimonial
)
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
        cleaned_data = super(ProfessionalExperienceForm, self).clean()
        if cleaned_data.get('end_date', None) is None and not cleaned_data.get('currently_working', None):
            self.add_error('end_date', _("End date is required if you are not currently working here."))
        elif cleaned_data.get('end_date') is not None and cleaned_data.get('currently_working'):
            self.add_error('end_date', _("End date is not required if you are currently working here."))
            self.add_error('currently_working', _("Currently working is not required if you provide an end date."))
            raise forms.ValidationError(
                _("Conflicting with `End date` and `Currently working`. Please specify only one.")
            )
        return cleaned_data

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date and end_date <= self.cleaned_data.get('start_date'):
            raise forms.ValidationError(_("End date must be greater than start date"))
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
        fields = ProfessionalExperienceForm.Meta.fields + ['file', ]

    def clean_file(self):
        file = self.cleaned_data.get('file')
        return get_validated_file(file)


# ----------------------------------------------------
# *** Education Forms ***
# ----------------------------------------------------

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'address', 'field_of_study',
                  'start_date', 'end_date', 'currently_studying', 'grade', 'activities', 'description']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'start_date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'end_date'}),
            'activities': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'cols': 2,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'cols': 3,
                }
            ),
        }

    def clean(self):
        cleaned_data = super(EducationForm, self).clean()
        if cleaned_data.get('end_date', None) is None and not cleaned_data.get('currently_studying', None):
            self.add_error('end_date', _("End date is required if you are not currently studying here."))
        elif cleaned_data.get('end_date') is not None and cleaned_data.get('currently_studying'):
            self.add_error('end_date', _("End date is not required if you are currently studying here."))
            self.add_error('currently_studying', _("Currently studying is not required if you provide an end date."))
            raise forms.ValidationError(
                _("Conflicting with `End date` and `Currently studying`. Please specify only one.")
            )
        return cleaned_data

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date and end_date <= self.cleaned_data.get('start_date'):
            raise forms.ValidationError(_("End date must be greater than start date"))
        return end_date


class EducationMediaForm(forms.ModelForm):
    class Meta:
        model = EducationMedia
        fields = ("file",)


class EducationWithMediaForm(EducationForm):
    """ EducationWithMediaForm = EducationForm + EducationMediaForm """

    # multiple file form field
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(EducationForm.Meta):
        fields = EducationForm.Meta.fields + ['file', ]

    def clean_file(self):
        file = self.cleaned_data.get('file')
        return get_validated_file(file)


# ----------------------------------------------------
# *** Certification Forms ***
# ----------------------------------------------------

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'organization', 'address', 'issue_date', 'expiration_date',
                  'does_not_expire', 'credential_id', 'credential_url', 'description']
        widgets = {
            'issue_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'issue_date'}),
            'expiration_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'expiration_date'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'cols': 3,
                }
            ),
        }

    def clean(self):
        cleaned_data = super(CertificationForm, self).clean()
        if cleaned_data.get('expiration_date', None) is None and not cleaned_data.get('does_not_expire', None):
            self.add_error('expiration_date', _("Expiration Date is required if this credential does expire."))
        elif cleaned_data.get('expiration_date') is not None and cleaned_data.get('does_not_expire'):
            self.add_error('expiration_date', _("Expiration Date is not required if this credential does not expire."))
            self.add_error('does_not_expire', _("Not required if you provide an Expiration Date."))
            raise forms.ValidationError(
                _("Conflicting with `Expiration Date` and `Does not expire`. Please specify only one.")
            )
        return cleaned_data

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date <= self.cleaned_data.get('issue_date'):
            raise forms.ValidationError(_("Expiration date must be greater than Issue date"))
        return expiration_date


class CertificationMediaForm(forms.ModelForm):
    class Meta:
        model = CertificationMedia
        fields = ("file",)


class CertificationWithMediaForm(CertificationForm):
    """ CertificationWithMediaForm = CertificationForm + CertificationMediaForm """

    # multiple file form field
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(CertificationForm.Meta):
        fields = CertificationForm.Meta.fields + ['file', ]

    def clean_file(self):
        file = self.cleaned_data.get('file')
        return get_validated_file(file)


# ----------------------------------------------------
# *** Project Forms ***
# ----------------------------------------------------

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'short_description', 'technology', 'start_date',
                  'end_date', 'currently_working', 'url', 'description']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'start_date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'end_date'}),
            'technology': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'cols': 2,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'cols': 3,
                }
            ),
        }

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        if cleaned_data.get('end_date', None) is None and not cleaned_data.get('currently_working', None):
            self.add_error('end_date', _("End date is required if you are not currently working on this project."))
        elif cleaned_data.get('end_date') is not None and cleaned_data.get('currently_working'):
            self.add_error('end_date', _("End date is not required if you are currently working on this project."))
            self.add_error('currently_working', _("Currently working is not required if you provide an end date."))
            raise forms.ValidationError(
                _("Conflicting with `End date` and `Currently working`. Please specify only one.")
            )
        return cleaned_data

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date and end_date <= self.cleaned_data.get('start_date'):
            raise forms.ValidationError(_("End date must be greater than start date"))
        return end_date


class ProjectMediaForm(forms.ModelForm):
    class Meta:
        model = ProjectMedia
        fields = ("file",)


class ProjectWithMediaForm(ProjectForm):
    """ ProjectWithMediaForm = ProjectForm + ProjectMediaForm """

    # multiple file form field
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(ProjectForm.Meta):
        fields = ProjectForm.Meta.fields + ['file', ]

    def clean_file(self):
        file = self.cleaned_data.get('file')
        return get_validated_file(file)


# ----------------------------------------------------
# *** Interest Forms ***
# ----------------------------------------------------

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ('title', 'icon')

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        return get_validated_image(icon)


# ----------------------------------------------------
# *** Testimonial Forms ***
# ----------------------------------------------------

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('name', 'designation', 'image', 'description')
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'cols': 3,
                }
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        return get_validated_image(image)
