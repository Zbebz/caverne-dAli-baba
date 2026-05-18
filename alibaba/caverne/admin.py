from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Fichier, Enseignant

admin.site.register(User, UserAdmin)
admin.site.register(Fichier)
admin.site.register(Enseignant)
