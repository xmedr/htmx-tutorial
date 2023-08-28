from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from htmx_tut.models import Task


class Home(TemplateView):
    template_name = 'htmx_tut/index.html'


class TaskListView(ListView):
    template_name = "htmx_tut/tasks.html"
    model = Task
    context_object_name = "tasks"


class TaskCreateView(CreateView):
    model = Task
    fields = ["description"]
    success_url = reverse_lazy("tasks")

    def post(self, request, *args, **kwargs):
        is_htmx = request.headers.get('HX-Request')
        form = self.get_form()
        if is_htmx and form.is_valid():
            print("IN THE CREATE AS AN HX-REQUEST")
            self.object = form.save()
            tasks = Task.objects.all()
            return render(request, "htmx_tut/task_list.html", {"tasks": tasks})
        else:
            return self.form_invalid(form)


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        success_url = self.get_success_url()
        is_htmx = self.request.headers.get('HX-Request')
        self.object.delete()
        if is_htmx:
            print("IN THE DELETE AS AN HX-REQUEST")
            tasks = Task.objects.all()
            return render(self.request, "htmx_tut/task_list.html", {"tasks": tasks})
        return HttpResponseRedirect(success_url)
        
    # def delete(self, request, *args, **kwargs):
    #     """
    #     Note: this works, but django complains with a DeleteViewCustomDeleteWarning
    #     """
    #     is_htmx = request.headers.get('HX-Request')
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     self.object.delete()
    #     if is_htmx:
    #         print("IN THE DELETE AS AN HX-REQUEST")
    #         tasks = Task.objects.all()
    #         return render(request, "htmx_tut/task_list.html", {"object_list": tasks})
    #     return HttpResponseRedirect(success_url)
        

def page_not_found(request, exception, template_name='htmx_tut/404.html'):
    return render(request, template_name, status=404)


def server_error(request, template_name='htmx_tut/500.html'):
    return render(request, template_name, status=500)
