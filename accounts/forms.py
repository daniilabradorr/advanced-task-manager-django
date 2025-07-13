from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }