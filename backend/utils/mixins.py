from django.views.generic import UpdateView, DetailView
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages


"""
----------------------- * Generic View Mixins * -----------------------
"""


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
----------------------- * Context Mixin for Generic Views * -----------------------
"""

class ContextMixinView():
    """
    This is a mixin for generic views.
    It adds contexts to the view.
    """

    additional_contexts = {}

    def get_context_data(self, **kwargs):

        try:
            context = super().get_context_data(**kwargs)
        except:
            context = {}

        context['meta_description'] = "numanibnmazid.com: Portfolio of Numan Ibn Mazid. A professional Software Engineer who enjoys developing innovative software solutions that are tailored to customer desirability and usability. Email: numanibnmazid@gmail.com"
        context['meta_keywords'] = "numan ibn mazid, portfolio, website, web application, software development, software developer, singer, musician, youtuber, django, django rest framework, python, data structure and algorithms"
        context["meta_author"] = "Numan Ibn Mazid"
        context["head_title"] = context["page_title"] = "Home"

        # check if view has context
        if hasattr(self, "get_additional_context_data"):
            additional_context_data = self.get_additional_context_data()
            for key, value in additional_context_data.items():
                context[key] = value

        # return the context data
        return context


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
