from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Fichier, Enseignant, Tag

admin.site.register(User)
admin.site.register(Fichier)
admin.site.register(Tag)
admin.site.register(Enseignant)
