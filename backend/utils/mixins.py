from django.views.generic.base import ContextMixin
from django.views.generic import UpdateView, DetailView, View, TemplateView, ListView, CreateView
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.http import HttpResponseForbidden
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

        # default app contexts
        default_app_contexts = {
            # meta description
            "meta_description": "numanibnmazid.com: Portfolio of Numan Ibn Mazid. A professional Software Engineer who enjoys developing innovative software solutions that are tailored to customer desirability and usability. Email: numanibnmazid@gmail.com",
            # meta keywords
            "meta_keywords": "numan ibn mazid, portfolio, website, web application, software development, software developer, singer, musician, youtuber, django, django rest framework, python, data structure and algorithms",
            # meta author
            "meta_author": "Numan Ibn Mazid",
            # meta copyright
            "meta_copyright": f"Numan Ibn Mazid, {now().year}",
            # meta robots
            "meta_robots": "index, follow",
            # meta googlebot
            "meta_googlebot": "index, follow",
            # page contexts
            "head_title": "Home",
            "page_title": "Home",
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


class CustomViewSetMixin(TemplateView, ListView, CreateView, UpdateView, DetailView, ContextMixinView, View):

    # default messages
    success_message = None
    error_message = None

    object = None
    object_list = None

    def get_success_url(self):
        look_up_field = self.look_up_field if hasattr(self, 'look_up_field') else None
        return reverse(self.success_url, kwargs={look_up_field: getattr(self.object, look_up_field)} if look_up_field else None)

    def get_for_queryset(self):
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
        context = self.get_context_data()
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        try:
            if self.get_object():
                self.object = self.get_object()
                return super().get(request, *args, **kwargs)
            else:
                return self.get_for_queryset()
        except:
            return self.get_for_queryset()

    def post(self, request, *args, **kwargs):
        action = "create" if request.method == "POST" else "update" if request.method == "PUT" else request.method
        success_message = self.success_message if self.success_message else f"{action.title()}d successfully" if action else "SUCCESS"
        error_message = self.error_message if self.error_message else f"Failed to {action.title()}" if action else "FAILED"

        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        try:
            self.object = self.get_object()
        # bypass
        except:
            pass

        form = self.get_form()

        if form.is_valid():
            messages.add_message(
                self.request, messages.SUCCESS, success_message
            )
            return self.form_valid(form)
        else:
            messages.add_message(
                self.request, messages.ERROR, error_message
            )
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class UpdateDetailMixinView(UpdateView, DetailView):

    success_message = "Updated Successfully"
    error_message = "Failed to Update"

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
