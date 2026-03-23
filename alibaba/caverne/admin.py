from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Fichier, Enseignant

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Fichier)
admin.site.register(Enseignant)
