#Para que rediriga cuando el register al board list
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # tras login o signup, ir al listado de tableros
        return reverse('boards:list')