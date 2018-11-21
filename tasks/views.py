from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import *


class TaskList(LoginRequiredMixin, generic.list.ListView):
    model = Task
    context_object_name = 'tasks'
    def get_queryset(self):
        return Task.objects.filter(done=False)

class TaskAll(LoginRequiredMixin, generic.list.ListView):
    model = Task
    context_object_name = 'tasks'

class TaskAdd(LoginRequiredMixin, generic.edit.CreateView):
    model = Task
    form_class = TaskForm

class TaskEdit(LoginRequiredMixin, generic.edit.UpdateView):
    model = Task
    form_class = TaskForm

class TaskComment(LoginRequiredMixin, generic.edit.UpdateView):
    model = Task
    form_class = CommentForm

class TaskDetail(LoginRequiredMixin, generic.detail.DetailView):
    model = Task

class TaskDone(LoginRequiredMixin, generic.base.RedirectView):
    url = '/tasks/list/undone'

    def get_redirect_url(self, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        task.done = True
        task.save()
        return super().get_redirect_url(*args, **kwargs)


class TaskDelete(LoginRequiredMixin, generic.edit.DeleteView):
    model = Task
