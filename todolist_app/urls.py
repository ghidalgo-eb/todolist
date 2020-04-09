from django.urls import path
from .views import (
    TodoListView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    TodoAssignUserView,
    TodoDetailView
)
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', TodoListView.as_view(), name='todo_list'),
    path('create/', TodoCreateView.as_view(), name='todo_create'),
    path('update/<pk>', TodoUpdateView.as_view(), name='todo_update'),
    path('delete/<pk>', TodoDeleteView.as_view(), name='todo_delete'),
    path('assign-user/<pk>', TodoAssignUserView.as_view(), name='todo_assign'),
    path('detail/<pk>/', TodoDetailView.as_view(), name='todo_detail'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
