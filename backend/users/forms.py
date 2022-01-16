from django import forms
from allauth.account.forms import LoginForm
from django.contrib.auth import get_user_model
from django.conf import settings
import os
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.template.defaultfilters import filesizeformat


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.EmailInput(
            attrs={
                'autocomplete': 'off', 'placeholder': 'Email Address', 'class': 'block w-full mb-4 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-app-theme-400 focus:outline-none focus:shadow-outline-app-theme dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            }
        )
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'autocomplete': 'off', 'placeholder': 'Password', 'class': 'block w-full mb-4 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-app-theme-400 focus:outline-none focus:shadow-outline-app-theme dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            }
        )

        # remove remember field checkbox and render manually in form
        if 'remember' in self.fields.keys():
            del self.fields['remember']

    def clean(self):
        cleaned_data = super(CustomLoginForm, self).clean()

        # remember me
        remember = False
        if self.request.POST.get('remember', None) == "on":
            remember = True
        self.cleaned_data.update({'remember': remember})

        # return cleaned data
        return cleaned_data


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = (
            'name', 'nick_name', 'gender', 'image', 'dob', 'website', 'contact', 'contact_email', 'address', 'about'
        )
        # widgets = {
        #     'dob': forms.DateInput(
        #         format=('%Y-%m-%d'),
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'Select a date',
        #             'type': 'date'
        #         }
        #     ),
        # }
        widgets = {
            'dob': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'datepicker',
                }
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and isinstance(image, UploadedFile):
            file_extension = os.path.splitext(image.name)[1]
            allowed_image_types = settings.ALLOWED_IMAGE_TYPES
            if not file_extension in allowed_image_types:
                raise forms.ValidationError("Only %s file formats are supported! Current image format is %s" % (
                    allowed_image_types, file_extension))
            if image.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image.size)))
        return image
