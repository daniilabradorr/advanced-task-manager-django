from django import forms
from .models import Task, Label

#Formulario personalizado de tarea
class TaskForm(forms.ModelForm):
    #Para que renderize la fecha limite como fecha
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'}),
        required=False,
        label = 'Fecha Límite'
    )

    #Para vincular el form al modelo
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'assignee',
            'priority',
            'labels',
            'due_date',
        ]
        #Widgets para 
        widgets = {
            'description': forms.Textarea(attrs={'rows':3}),
            'labels': forms.CheckboxSelectMultiple,
        }