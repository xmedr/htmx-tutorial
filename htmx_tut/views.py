from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'htmx_tut/index.html'


def page_not_found(request, exception, template_name='htmx_tut/404.html'):
    return render(request, template_name, status=404)


def server_error(request, template_name='htmx_tut/500.html'):
    return render(request, template_name, status=500)
