from django.contrib import admin
from .models import Board
from tasks.models import TaskList,Task

class TaskListInline(admin.TabularInline):
    model = TaskList
    extra = 0
    fields = ('name', 'position')
    show_change_link = True

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug','created')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'owner__username')
    inlines = [TaskListInline]