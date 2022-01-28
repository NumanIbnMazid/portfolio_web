from django.core.exceptions import ValidationError
from django.views.generic.base import ContextMixin
from django.views.generic import UpdateView, TemplateView, ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ImproperlyConfigured
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

        # Assuring if defined success_url as it has other dependencies
        if self.success_url is None:
            raise ImproperlyConfigured(_("Requires either a definition of `success_url`"))

        try:
            context = super().get_context_data(**kwargs)
        except:
            context = {}

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
            "snippet_template": self.snippet_template if hasattr(self, "snippet_template") else None,
            f"{self.model.__name__}_url_list": self.url_list if hasattr(self, "url_list") else [],
            "url_list": self.url_list if hasattr(self, "url_list") else [],
            "display_fields": self.model._meta.get_fields(),
            "action": self.action if self.action else None,
            # head & page title
            "head_title": _(f"{getattr(self.model._meta, 'verbose_name_plural', f'{self.model.__name__} List')}" if self.action and self.action == "list" else f"{getattr(self.model._meta, 'verbose_name', f'{self.model.__name__}')} Detail" if self.action and self.action == "detail" else f"{self.action.title()} {getattr(self.model._meta, 'verbose_name', {self.model.__name__})}" if self.action else "Home"),
            "page_title": _(f"{getattr(self.model._meta, 'verbose_name_plural', f'{self.model.__name__} List')}" if self.action and self.action == "list" else f"{getattr(self.model._meta, 'verbose_name', f'{self.model.__name__}')} Detail" if self.action and self.action == "detail" else f"{self.action.title()} {getattr(self.model._meta, 'verbose_name', {self.model.__name__})}" if self.action else "Home"),
            # Object List URL
            "object_list_url": self.success_url,
        }

        # synchornize default app contexts with context
        context.update(default_app_contexts)

        # check if view has context
        if hasattr(self, "get_additional_context_data"):
            additional_context_data = self.get_additional_context_data()
            for key, value in additional_context_data.items():
                context[key] = value

        # look up for custom action method's context data
        if self.action and hasattr(self, f"get_{self.action}_context_data"):
            # call action method
            action_context_data = getattr(self, f"get_{self.action}_context_data")(**kwargs)
            for key, value in action_context_data.items():
                context[key] = value

        # synchronize kwargs with default app context
        context.update(kwargs)

        # return contexts
        return context


class CustomViewSetMixin(UpdateView, ListView, TemplateView, ContextMixinView):

    success_url = None
    lookup_field = 'pk'

    # default messages
    success_message = None
    error_message = None

    object = None
    object_list = None

    # action (expected to be passed in as_view() method from urls.py)
    action = None

    # page specific templates
    snippet_template = None

    def get_success_url(self):
        look_up_field = self.look_up_field if hasattr(self, 'look_up_field') else None
        URL = reverse(self.success_url, kwargs={look_up_field: getattr(self.object, look_up_field)} if look_up_field else None)
        # add pagination data with url if any
        if 'page' in self.request.GET:
            URL += f"?page={self.request.GET['page']}"
        return URL

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
            try:
                return super().get(request, *args, **kwargs)
            except Exception as exception:
                if "That page contains no results" in str(exception):
                    return HttpResponseRedirect(reverse(self.success_url))

                print("**************************************** EXCEPTION ****************************************")
                print(exception)
                print("**************************************** EXCEPTION ****************************************")

                messages.add_message(
                    self.request, messages.ERROR, _("Something went wrong. Please try again later.")
                )
                return HttpResponseRedirect(reverse('home'))

    def post(self, request, *args, **kwargs):
        # handle actions
        # handle delete action
        if self.action and self.object and self.action == "delete":
            # call delete method
            return self.delete(request, *args, **kwargs)

        # handle custom action method
        elif self.action and hasattr(self, f"{self.action}"):
            # call action method
            return getattr(self, f"{self.action}")(request, *args, **kwargs)

        try:
            self.object = self.get_object()
        # bypass
        except:
            pass

        form = self.get_form()

        # assign object_list
        self.object_list = self.get_queryset()

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
                # call model's `validate_unique()` method to validate `unique_together`
                # this will also raise a `ValidationError` instead of default `IntegrityError`
                form.instance.validate_unique()
                # If the form is valid, save the associated model.
                self.object = form.save()
                # add success message
                messages.add_message(
                    self.request, messages.SUCCESS, self.get_success_message()
                )
                return super().form_valid(form)

        except Exception as exception:
            print("**************************************** EXCEPTION ****************************************")
            print(exception)
            print("**************************************** EXCEPTION ****************************************")

            # call custom exception message handler to generate message
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
                                return
                        else:
                            messages.add_message(
                                self.request, messages.ERROR, value
                            )
                            return
            else:
                messages.add_message(
                    self.request, messages.ERROR, exception.message
                )
                return
        messages.add_message(
            self.request, messages.ERROR, self.get_error_message()
        )
        return

    def get_success_message(self):
        if self.action and hasattr(self, f"{self.action}_success_message"):
            return getattr(self, f"{self.action}_success_message", "SUCCESS")
        elif self.success_message:
            return self.success_message
        elif self.action:
            return _(f"{getattr(self.model._meta, 'verbose_name', {self.model.__name__}).title()} {self.action.title()}d Successfully")
        else:
            return _("SUCCESS")

    def get_error_message(self):
        if self.action and hasattr(self, f"{self.action}_error_message"):
            return getattr(self, f"{self.action}_error_message", "ERROR")
        elif self.error_message:
            return self.error_message
        elif self.action:
            return _(f"Failed to {self.action.title()} {getattr(self.model._meta, 'verbose_name', {self.model.__name__}).title()}")
        else:
            return _("ERROR")


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
