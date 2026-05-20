from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import FichierForm, RegisterForm
from .models import Enseignant


@login_required
def index(request):
    return render(request, "caverne/index.html")

@login_required
def upload(request):
    if request.method == "POST":
        fichier = FichierForm(request.POST, request.FILES)
        if fichier.is_valid():
            fichier = fichier.save(commit=False)
            fichier.user = request.user
            fichier.save()

            teacher = Enseignant.objects.get_or_create(name=fichier.enseignant)[0]
            teacher.ecole = fichier.ecole
            teacher.save()
            return redirect(reverse("index"))
    else:
        fichier = FichierForm()
    return render(request, "caverne/upload.html", {"form": fichier})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))
    else:
        form = RegisterForm()

    return render(request, "caverne/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(reverse("index"))
