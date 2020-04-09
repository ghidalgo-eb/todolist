from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import TodoList
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class TodoListView(LoginRequiredMixin, ListView):

    paginate_by = 3
    model = TodoList

    def get_queryset(self):
        return TodoList.objects.filter(assigned_user=self.request.user)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = TodoList
    fields = ['title', 'Description', 'done', 'priority']

    def get_success_url(self):
        return reverse('todo_detail', args=(self.object.id,))

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        form.instance.assigned_user = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = TodoList
    fields = ['title', 'Description', 'done', 'priority']

    def get_object(self):
        todo = super().get_object()
        if todo.assigned_user.id != self.request.user.id:
            raise PermissionDenied
        return todo

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        form.instance.assigned_user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('todo_detail', args=(self.object.id,))


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = TodoList
    success_url = reverse_lazy('todo_list')

    def get_object(self):
        todo = super().get_object()
        if todo.assigned_user.id != self.request.user.id:
            raise PermissionDenied
        return todo


class TodoAssignUserView(LoginRequiredMixin, UpdateView):
    model = TodoList
    fields = ['assigned_user']

    def get_success_url(self):
        return reverse('todo_detail', args=(self.object.id,))


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = TodoList

