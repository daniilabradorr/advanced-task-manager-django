from rest_framework import serializers
from .models import TaskList, Task

#Serializr personaliado para klista de tareas y para tarea
class TaskListSerializer(serializers.ModelSerializer):
    """
    Serializer para reordenación de TaskList:
      - Solo exponemos 'position' (la nueva posición).
      - 'id' para identificar qué lista estamos moviendo.
    """
    class Meta:
        model = TaskList
        fields = ['id','position']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer para reordenación de Task:
      - 'id' identifica la tarea.
      - 'position' es su posición en la lista.
      - 'task_list' es el ID de la lista destino.
    """
    class Meta:
        model = Task
        fields = ['id','position','task_list']

#Todo esto lo hago apra transformar las instacinas a JSON y validar los campos que se van actualizar