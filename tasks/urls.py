from django.urls import path
from .views import TaskCreateView, TaskUpdateView, TaskDeleteView
from .api import TaskListReorderAPI, TaskReorderAPI

app_name = 'tasks'

urlpatterns = [
    path('lists/<int:pk>/tasks/add/', TaskCreateView.as_view(), name='add'),
    path('tasks/<int:pk>/edit/',   TaskUpdateView.as_view(), name='edit'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),

    # PARA LA API DE REORDENACION
    path('api/tasklists/<int:pk>/move/', TaskListReorderAPI.as_view(),
         name='api-tasklist-move'),
    path('api/tasks/<int:pk>/move/',     TaskReorderAPI.as_view(),
         name='api-task-move'),

]