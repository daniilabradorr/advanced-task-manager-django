from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

#Personalizacdo User para que aparezca en el admin de DJANGO
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Extras', {
            "fields": ('avatar', 'bio'),
        }),
    )