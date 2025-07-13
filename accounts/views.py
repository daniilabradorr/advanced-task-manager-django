# accounts/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from .models import User
from .forms import ProfileForm


#VIsta para mostrar el perfil de usuarrio
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.request.user
        return data


#VIsta poara editar algun dato del perfil del usuario
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'account/profile_edit.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "✅ Tu perfil ha sido actualizado correctamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "⚠️ Hubo un error al actualizar tu perfil. Por favor revisa los datos.")
        return super().form_invalid(form)
