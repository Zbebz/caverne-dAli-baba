from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import FichierForm

# Create your views here.
def index(request):
    return render(request, "caverne/index.html")

def upload(request):
    if request.method == "POST":
        form = FichierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(reverse('index'))
    else:
        form = FichierForm()
    return render(request, "caverne/upload.html", {'form': form})