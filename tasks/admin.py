from django.contrib import admin
from .models import TaskList, Task

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('title', 'assignee', 'position', 'priority', 'due_date')
    show_change_link = True

@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'position')
    list_filter = ('board',)
    search_fields = ('name',)
    inlines = [TaskInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_list', 'assignee', 'position', 'priority', 'due_date')
    list_filter = ('assignee', 'priority', 'task_list__board')
    search_fields = ('title', 'description')
    ordering = ('task_list', 'position')
