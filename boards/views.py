from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from .models import Board
from tasks.models import Task
from tasks.models import TaskList

#Para la exportacion en vsc o json de las tareas
import csv
from django.http import HttpResponse, JsonResponse

# Vista de la lista de tableros
# Esta vista muestra todos los tableros a los que el usuario tiene acceso
class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    template_name = 'boards/board_list.html'
    context_object_name = 'boards'
    
    def get_queryset(self):
        return Board.objects.filter(
            Q(owner=self.request.user) |     # uso Q directamente
            Q(members=self.request.user)
        ).distinct()
    

# Clase para ver los detalles de un tablero
class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = 'boards/board_detail.html'
    context_object_name = 'board'

    def get_queryset(self):
        return Board.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        board = self.get_object()

        # Leemos 'priority' del querystring (valor "1","2" o "3")
        selected = self.request.GET.get('priority', '')
        ctx['selected_priority'] = selected

        # Preparamos las listas con tareas filtradas por prioridad
        lists = board.lists.all()
        for lst in lists:
            if selected in ['1', '2', '3']:
                lst.filtered_tasks = (
                    lst.tasks
                       .filter(priority=int(selected))
                       .order_by('position')
                )
            else:
                lst.filtered_tasks = lst.tasks.all().order_by('position')
        ctx['lists'] = lists
        return ctx
    

# Clase para crear un nuevo tablero
class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    fields = ['name', 'slug', 'members']
    template_name = 'boards/board_form.html'
    # Redirige al detalle del tablero recién creado
    def get_success_url(self):
        return reverse_lazy('boards:detail', args=[self.object.slug])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"✅ Tablero «{form.instance.name}» creado.")
        return response
    

    def form_invalid(self, form):
        messages.error(self.request, "⚠️ Error al crear el tablero. Revisa los campos.")
        return super().form_invalid(form)
    

# Clase para actualizar un tablero ya existente
class BoardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Board
    fields = ['name', 'slug', 'members']
    template_name = 'boards/board_form.html'
    # Redirige al detalle del tablero actualizado
    def get_success_url(self):
        return reverse_lazy('boards:detail', args=[self.object.slug])

    def test_func(self):
        return self.get_object().owner == self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"✅ Tablero «{form.instance.name}» actualizado.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "⚠️ Error al actualizar el tablero.")
        return super().form_invalid(form)

# Clase para eliminar un tablero
class BoardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Board
    template_name = 'boards/board_confirm_delete.html'
    success_url = reverse_lazy('boards:list')

    def test_func(self):
        return self.get_object().owner == self.request.user

    def post(self, request, *args, **kwargs):
        # Al recibir el POST del formulario de confirmación:
        board = self.get_object()
        messages.success(request, f"🗑️ Tablero «{board.name}» eliminado.")
        return super().post(request, *args, **kwargs)
    

# Clase para crear las listas de tareas dentro de un tablero
class TaskListCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        board = get_object_or_404(Board, slug=slug)
        name = request.POST.get('name', '').strip()
        if name:
            position = board.lists.count() + 1
            TaskList.objects.create(board=board, name=name, position=position)
            messages.success(request, f"✅ Lista «{name}» añadida a «{board.name}».")
        else:
            messages.error(request, "⚠️ El nombre de la lista no puede estar vacío.")
        return redirect('boards:detail', slug=slug)



#Vista para editar la lista de tareas de l board
class TaskListUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TaskList
    fields = ['name']
    template_name = 'boards/tasklist_form.html'

    def get_success_url(self):
        # Vuelvo al detalle de su board
        return reverse_lazy('boards:detail', args=[self.object.board.slug])

    def test_func(self):
        tl = self.get_object()
        # Solo el owner del board puede editar sus listas
        return tl.board.owner == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
            f"✏️ Lista «{form.instance.name}» actualizada.")
        return response

    def form_invalid(self, form):
        messages.error(self.request,
            "⚠️ Error al actualizar la lista.")
        return super().form_invalid(form)


#Vista para borrar la lista de tareas del board
class TaskListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TaskList
    template_name = 'boards/tasklist_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('boards:detail',
                            args=[self.object.board.slug])

    def test_func(self):
        tl = self.get_object()
        return tl.board.owner == self.request.user

    def post(self, request, *args, **kwargs):
        tl = self.get_object()
        messages.success(request,
            f"🗑️ Lista «{tl.name}» eliminada.")
        return super().post(request, *args, **kwargs)
    


#Vista para la exportacion de las tareas en JSON / CSV
class ExportTasksView(LoginRequiredMixin, View):
    """
    GET /boards/<slug>/export/?format=csv|json
    Esto devuelve todas las tareas de un board en CSV o JSON.
    """
    def get(self, request, slug):
        board = get_object_or_404(Board, slug=slug)
        # Comprobar permisos
        if not (board.owner == request.user or request.user in board.members.all()):
            return HttpResponse(status=403)

        qs = Task.objects.filter(task_list__board=board) \
                         .order_by('task_list__position', 'position')
        fmt = request.GET.get('format', 'csv').lower()

        if fmt == 'json':
            data = [
                {
                    'lista':     t.task_list.name,
                    'titulo':    t.title,
                    'asignado':  t.assignee.username if t.assignee else None,
                    'prioridad': t.get_priority_display(),
                    'vencimiento': t.due_date.isoformat() if t.due_date else None,
                }
                for t in qs
            ]
            return JsonResponse(data, safe=False)

        # CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{board.slug}_tasks.csv"'
        writer = csv.writer(response)
        writer.writerow(['Lista','Título','Asignado','Prioridad','Fecha límite'])
        for t in qs:
            writer.writerow([
                t.task_list.name,
                t.title,
                t.assignee.username if t.assignee else '',
                t.get_priority_display(),
                t.due_date or '',
            ])
        return response