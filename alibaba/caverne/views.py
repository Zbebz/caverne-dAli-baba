from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import FichierForm
from .models import Fichier, User
# Create your views here.
def index(request):
    return render(request, "caverne/index.html")

def upload(request):
    testuser = User.objects.get(username="test")
    if request.method == "POST":
        form = FichierForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = testuser
            form.save()
            return redirect(reverse('index'))
    else:
        form = FichierForm()
    return render(request, "caverne/upload.html", {'form': form})