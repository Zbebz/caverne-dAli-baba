from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import FichierForm
from .models import Enseignant, User


def index(request):
    return render(request, "caverne/index.html")


def upload(request):
    testuser = User.objects.get_or_create(username="test")[0]
    if request.method == "POST":
        fichier = FichierForm(request.POST, request.FILES)
        if fichier.is_valid():
            fichier = fichier.save(commit=False)
            fichier.user = testuser
            print(fichier)
            fichier.save()

            teacher = Enseignant.objects.get_or_create(name=fichier.enseignant)[0]
            teacher.ecole = fichier.ecole
            teacher.save()
            return redirect(reverse("index"))
    else:
        fichier = FichierForm()
    return render(request, "caverne/upload.html", {"form": fichier})
