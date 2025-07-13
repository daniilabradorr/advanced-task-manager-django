from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib import messages

from tasks.models import Task, TaskList
from tasks.forms import TaskForm
from boards.models import Board


#Vista de tarea para crearlas
class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    #Capturo Tasklist padre anets de procesor GET/POST
    def dispatch(self, request, *args, **kwargs):
        self.task_list = get_object_or_404(TaskList, pk = self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    #Asocio la nueva tarea a la Tasklist y le doy posicion al final
    def form_valid(self, form):
        form.instance.task_list = self.task_list
        form.instance.position = self.task_list.tasks.count()+1
        response = super().form_valid(form)
        messages.success(self.request, f"✅ Tarea «{form.instance.title}» creada.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "⚠️ Error al crear la tarea. Revisa los campos.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        #Volver al detalle del board
        return reverse_lazy('boards:detail',args = [self.task_list.board.slug])
    

#Vista para editar actualizar una tarea
class TaskUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def test_func(self):
        #Solo el Owner o miembros que puedan editar
        board = self.get_object().task_list.board
        return board.owner == self.request.user or self.request.user in board.members.all()
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"✅ Tarea «{form.instance.title}» actualizada.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "⚠️ Error al actualizar la tarea.")
        return super().form_invalid(form)

    def get_success_url(self):
        tl = self.get_object().task_list
        return reverse_lazy('boards:detail', args=[tl.board.slug])
    

#Vista para eliminar una tarea
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'

    def test_func(self):
        board = self.get_object().task_list.board
        return board.owner == self.request.user or self.request.user in board.members.all()

    def post(self, request, *args, **kwargs):
        # Al recibir el POST para borrar
        task = self.get_object()
        messages.success(request, f"🗑️ Tarea «{task.title}» eliminada.")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        tl = self.get_object().task_list
        return reverse_lazy('boards:detail', args=[tl.board.slug])



    
    
