from django.urls import path
from .views import (
    BoardListView, BoardDetailView,
    BoardCreateView, BoardUpdateView, BoardDeleteView,
    TaskListCreateView, TaskListDeleteView, TaskListUpdateView, ExportTasksView
)

app_name = 'boards'
urlpatterns = [
    path('', BoardListView.as_view(), name='list'),
    path('create/', BoardCreateView.as_view(), name='create'),
    path('<slug:slug>/', BoardDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', BoardUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', BoardDeleteView.as_view(), name='delete'),
    path('<slug:slug>/lists/add/', TaskListCreateView.as_view(), name='tasklist_add'),
    path('<slug:slug>/lists/<int:pk>/edit/',
         TaskListUpdateView.as_view(), name='tasklist_edit'),
    path('<slug:slug>/lists/<int:pk>/delete/',
         TaskListDeleteView.as_view(), name='tasklist_delete'),
    path('<slug:slug>/export/',    ExportTasksView.as_view(),   name='export'),
]