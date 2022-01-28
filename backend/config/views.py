from django.views.generic import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, "pages/index.html", context=context)

    def get_context_data(self, **kwargs):
        context = {}
        context['meta_description'] = "numanibnmazid.com: Portfolio of Numan Ibn Mazid. A professional Software Engineer who \
        enjoys developing innovative software solutions that are tailored to customer desirability and usability. \
        Email: numanibnmazid@gmail.com"
        context['meta_keywords'] = "numan ibn mazid, portfolio, website, web application, software development, \
        software developer, singer, musician, youtuber, django, django rest framework, python, data structure and algorithms"
        context["meta_author"] = "Numan Ibn Mazid"
        # page contexts
        context["head_title"] = "Home"
        return context


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, "admin-panel/pages/index.html", context=context)

    def get_context_data(self, **kwargs):
        context = {}
        context['meta_description'] = "numanibnmazid.com: Portfolio of Numan Ibn Mazid. A professional Software Engineer \
        who enjoys developing innovative software solutions that are tailored to customer desirability and usability. \
        Email: numanibnmazid@gmail.com"
        context['meta_keywords'] = "numan ibn mazid, portfolio, website, web application, software development, \
        software developer, singer, musician, youtuber, django, django rest framework, python, data structure and algorithms"
        context["meta_author"] = "Numan Ibn Mazid"
        # page contexts
        context["head_title"] = "Dashboard"
        return context
