from django.db import models
from django.conf import settings

#Clase de lista de tareas
class TaskList(models.Model):
    board = models.ForeignKey('boards.Board', related_name='lists', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #Para ordenarlas por posicion
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name


#clase personalizada de la etiqueta
class Label (models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#29b6f6')

    def __str__(self):
        return self.name
    

# Clase principal de la tarea
class Task(models.Model):
    task_list = models.ForeignKey(TaskList, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_tasks', null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.PositiveSmallIntegerField(choices=[(1,'Alta'),(2,'Media'),(3,'Baja')], default=2)
    labels = models.ManyToManyField(Label,blank=True)
    due_date = models.DateField(null=True, blank=True)
    position = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title