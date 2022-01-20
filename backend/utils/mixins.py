from django.core.exceptions import ValidationError
from django.views.generic.base import ContextMixin
from django.views.generic import UpdateView, DetailView, TemplateView, ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.contrib import messages
from utils.helpers import now


"""
----------------------- * Generic View Mixins * -----------------------
"""

class ContextMixinView(ContextMixin):
    """
    This is a mixin for generic views.
    It adds contexts to the view.
    """

    def get_context_data(self, **kwargs):
        """Insert custom contexts into the context dict."""

        try:
            context = super().get_context_data(**kwargs)
        except:
            context = {}
        # define urls
        skill_urls = ["skills", "skill_create", "skill_detail", "skill_update", "skill_delete"]
        # default app contexts
        default_app_contexts = {
            # meta description
            "meta_description": _("numanibnmazid.com: Portfolio of Numan Ibn Mazid. A professional Software Engineer who enjoys developing innovative software solutions that are tailored to customer desirability and usability. Email: numanibnmazid@gmail.com"),
            # meta keywords
            "meta_keywords": _("numan ibn mazid, portfolio, website, web application, software development, software developer, singer, musician, youtuber, django, django rest framework, python, data structure and algorithms"),
            # meta author
            "meta_author": _("Numan Ibn Mazid"),
            # meta copyright
            "meta_copyright": _(f"Numan Ibn Mazid, {now().year}"),
            # meta robots
            "meta_robots": "index, follow",
            # meta googlebot
            "meta_googlebot": "index, follow",
            # page contexts
            "skill_urls": skill_urls,
            "portfolio_urls": skill_urls,
            "display_fields": self.model._meta.get_fields(),
            "action": self.action if self.action else None,
            "head_title": _(f"{getattr(self.model._meta, 'verbose_name_plural', f'{self.model.__name__} List')}" if self.action and self.action == "list" else f"{getattr(self.model._meta, 'verbose_name', f'{self.model.__name__}')} Detail" if self.action and self.action == "detail" else f"{self.action.title()} {str(self.model.__name__).title()}" if self.action else "Home"),
            "page_title": _(f"{getattr(self.model._meta, 'verbose_name_plural', f'{self.model.__name__} List')}" if self.action and self.action == "list" else f"{getattr(self.model._meta, 'verbose_name', f'{self.model.__name__}')} Detail" if self.action and self.action == "detail" else f"{self.action.title()} {str(self.model.__name__).title()}" if self.action else "Home"),
        }

        # synchornize the default app context with the context
        context.update(default_app_contexts)

        # check if view has context
        if hasattr(self, "get_additional_context_data"):
            additional_context_data = self.get_additional_context_data()
            for key, value in additional_context_data.items():
                context[key] = value

        # synchroneize the kwargs with the default app context
        context.update(kwargs)

        # return contexts
        return context


class CustomViewSetMixin(UpdateView, DetailView, ListView, TemplateView, ContextMixinView):

    # default messages
    success_message = None
    error_message = None

    object = None
    object_list = None

    # action (expected to be passed in as_view() method from urls.py)
    action = None

    def get_success_url(self):
        look_up_field = self.look_up_field if hasattr(self, 'look_up_field') else None
        return reverse(self.success_url, kwargs={look_up_field: getattr(self.object, look_up_field)} if look_up_field else None)

    def get(self, request, *args, **kwargs):
        try:
            if self.get_object():
                self.object = self.get_object()
        except:
            # pass except block
            pass
        # do the rest in finally block
        finally:
            self.object_list = self.get_queryset()
            allow_empty = self.get_allow_empty()

            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                        'class_name': self.__class__.__name__,
                    })

            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        # bypass
        except:
            pass

        form = self.get_form()

        # assign object_list
        self.object_list = self.get_queryset()

        if self.action and self.object and self.action == "delete":
            # call delete method
            return self.delete(request, *args, **kwargs)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object:
                self.object.delete()
                messages.add_message(
                    self.request, messages.SUCCESS, self.get_success_message()
                )
            else:
                raise Http404(_("Object not found!"))
        except:
            messages.add_message(
                self.request, messages.ERROR, self.get_error_message()
            )
        return HttpResponseRedirect(success_url)

    def form_valid(self, form):
        try:
            if form.is_valid():
                # call model's full_clean method to validate required additional validations
                form.instance.full_clean()
                # If the form is valid, save the associated model.
                self.object = form.save()

                messages.add_message(
                    self.request, messages.SUCCESS, self.get_success_message()
                )
                return super().form_valid(form)

        except Exception as exception:
            self.get_exception_message(form=form, exception=exception)
            return super().form_invalid(form)

        return super().form_invalid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR, self.get_error_message()
        )
        return super().form_invalid(form)

    def get_exception_message(self, form, exception):
        # check if the exception is a django.core.exceptions.ValidationError
        if isinstance(exception, ValidationError):
            # check if error is dict
            if isinstance(exception.message_dict, dict):
                for key, value in exception.message_dict.items():
                    # check if the key is in the form
                    if key in form.fields or key in ["__all__"]:
                        # check if value is a list
                        if isinstance(value, list):
                            for message in value:
                                messages.add_message(
                                    self.request, messages.ERROR, message
                                )
                        else:
                            messages.add_message(
                                self.request, messages.ERROR, value
                            )
            else:
                messages.add_message(
                    self.request, messages.ERROR, exception.message
                )
        else:
            messages.add_message(
                self.request, messages.ERROR, self.get_error_message()
            )

    def get_success_message(self):
        if self.action and hasattr(self, f"{self.action}_success_message"):
            return getattr(self, f"{self.action}_success_message", "SUCCESS")
        elif self.success_message:
            return self.success_message
        elif self.action:
            return _(f"{str(self.model.__name__).title()} {self.action.lower().title()}d successfully")
        else:
            return _("SUCCESS")

    def get_error_message(self):
        if self.action and hasattr(self, f"{self.action}_error_message"):
            return getattr(self, f"{self.action}_error_message", "ERROR")
        elif self.error_message:
            return self.error_message
        elif self.action:
            return _(f"Failed to {self.action} {str(self.model.__name__).title()}")
        else:
            return _("ERROR")

class UpdateDetailMixinView(UpdateView, DetailView):

    success_message = _("Updated Successfully")
    error_message = _("Failed to Update")

    def get_success_url(self):
        look_up_field = self.look_up_field if hasattr(self, 'look_up_field') else None
        return reverse(self.success_url, kwargs={look_up_field: getattr(self.object, look_up_field)} if look_up_field else None)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.add_message(
                self.request, messages.SUCCESS, self.success_message
            )
            return self.form_valid(form)
        else:
            messages.add_message(
                self.request, messages.ERROR, self.error_message
            )
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


"""
----------------------- * Custom Model Admin Mixins * -----------------------
"""


class CustomModelAdminMixin(object):
    '''
    DOCSTRING for CustomModelAdminMixin:
    This model mixing automatically displays all fields of a model in admin panel following the criteria.
    code: @ Numan Ibn Mazid
    '''

    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.get_internal_type() != 'TextField'
        ]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)
