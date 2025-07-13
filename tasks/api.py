from rest_framework.views import APIView #Importo la viosta api general de rest
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import TaskList, Task
from .serializers import TaskListSerializer, TaskSerializer


#Vista de la API de la lista de tareas y su reordenacion
class TaskListReorderAPI(APIView):
    """
    Endpoint PATCH /api/tasklists/<pk>/move/
    Permite actualizar la posición de una TaskList dentro de su Board.
    """
    permission_classes = [permissions.IsAuthenticated] #Si esta autenticado para hacerlo

    def patch(self, request, pk):
        #Obtengo la lista o error 404
        tl = get_object_or_404(TaskList, pk = pk)
        board = tl.board

        #Compruebo que le usuario pertenece al board
        if not (board.owner == request.user or request.user in board.members.all()):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        #Deserializo solo el position
        serializer = TaskListSerializer(tl, data = request.data, partial= True)
        serializer.is_valid(raise_exception = True)
        serializer.save() #De esta manera actualizo la position

        #Reajusto todas las posiciones para elminar huecos o dyuplicados
        lists = board.lists.order_by('position')
        for idx, lst in enumerate(lists,start=1):
            if lst.position != idx:
                lst.position = idx
                lst.save(update_fields=['position'])

        #Devuelvo el JSON con la TaskList modificada
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#Vista de la api para las tareas y su reordenacion
class TaskReorderAPI(APIView):
    """
    Endpoint PATCH /api/tasks/<pk>/move/
    Permite mover una Task dentro de la misma lista o a otra lista.
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self,request, pk):
        #Obtengp la tarea o el error 404
        task = get_object_or_404(Task, pk = pk)
        board = task.task_list.board

        #Verifico los permisos del usuario
        if not (board.owner == request.user or request.user in board.members.all()):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        #Deserializo los cambios (task_list nuevo o/y position nuevo)
        serializer = TaskSerializer(task, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save() #Actualiza task.task_list o/y position

        #Reajusto posiciones en la lista de origen y lista de destino. Para ello voy a crear un conjunto de ambas listas para poder iterar sobre ellas
        lists_to_fix = {
            task.task_list,
            board.lists.get(pk = request.data.get('task_list'))
        }
        for lst in lists_to_fix:
            for idx,t in enumerate(lst.tasks.order_by('position'), start=1):
                if t.position != idx:
                    t.position = idx
                    t.save(update_fields=['position'])

        return Response(serializer.data, status=status.HTTP_200_OK)