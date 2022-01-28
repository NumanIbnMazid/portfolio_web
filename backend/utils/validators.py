from django.conf import settings
import os
from django.core.files.uploadedfile import UploadedFile
from django.template.defaultfilters import filesizeformat
from django import forms


# allowed image types
ALLOWED_IMAGE_TYPES = settings.ALLOWED_IMAGE_TYPES if settings.ALLOWED_IMAGE_TYPES else []
# allowed document types
ALLOWED_DOCUMENT_TYPES = settings.ALLOWED_DOCUMENT_TYPES if settings.ALLOWED_DOCUMENT_TYPES else []
# allowed file types (all)
ALLOWED_FILE_TYPES = ALLOWED_IMAGE_TYPES + ALLOWED_DOCUMENT_TYPES

# maximum file upload size in bytes
MAX_UPLOAD_SIZE = settings.MAX_UPLOAD_SIZE if settings.MAX_UPLOAD_SIZE else 2621440


def get_validated_file(file):
    if file and isinstance(file, UploadedFile):
        file_extension = os.path.splitext(file.name)[1]
        allowed_file_types = ALLOWED_FILE_TYPES
        if file_extension not in allowed_file_types:
            raise forms.ValidationError(
                "Only %s file formats are supported! Current file format is %s" % (
                    allowed_file_types, file_extension if file_extension else "undefined"
                )
            )
        if file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Please keep file size under %s. Current file (%s) size is %s" % (
                    filesizeformat(MAX_UPLOAD_SIZE), file.name, filesizeformat(file.size)
                )
            )
    return file


def get_validated_image(image):
    if image and isinstance(image, UploadedFile):
        file_extension = os.path.splitext(image.name)[1]
        allowed_image_types = ALLOWED_IMAGE_TYPES
        if file_extension not in allowed_image_types:
            raise forms.ValidationError(
                "Only %s image formats are supported! Current file format is %s" % (
                    allowed_image_types, file_extension if file_extension else "undefined"
                )
            )
        if image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Please keep file size under %s. Current file (%s) size is %s" % (
                    filesizeformat(MAX_UPLOAD_SIZE), image.name, filesizeformat(image.size)
                )
            )
    return image


def get_validated_document(document):
    if document and isinstance(document, UploadedFile):
        file_extension = os.path.splitext(document.name)[1]
        allowed_document_types = ALLOWED_DOCUMENT_TYPES
        if file_extension not in allowed_document_types:
            raise forms.ValidationError(
                "Only %s document formats are supported! Current file format is %s" % (
                    allowed_document_types, file_extension if file_extension else "undefined"
                )
            )
        if document.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Please keep file size under %s. Current file (%s) size is %s" % (
                    filesizeformat(MAX_UPLOAD_SIZE), document.name, filesizeformat(document.size)
                )
            )
    return document
