from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .decorators import unauth_required, verified_required
from .forms import FichierForm, RegisterForm
from .models import Enseignant
from .tokens import account_activation_token


@login_required
@verified_required
def index(request):
    return render(request, "caverne/index.html")

@login_required
@verified_required
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

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, OverflowError, ValueError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        user.save()

        login(request, user)
        messages.success(
            request,
            "Vous pouvez maintenant accéder aux trésors de la caverne :)",
        )
    else:
        messages.error(request, "Ce lien est invalide")

    return render(request, "caverne/verification.html", {"messages": messages.get_messages(request)})

@unauth_required
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            message = render_to_string(
                "caverne/verification_email.html",
                {
                    "user": user,
                    "domain": get_current_site(request).domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                    "protocol": "https" if request.is_secure() else "http",
                },
            )
            email = EmailMessage(
                "Vérifiez votre compte",
                message,
                to=[user.email],
                reply_to=["no-reply@caverne.ch"],
            ) 
            email.content_subtype = "html" # https://sendlayer.com/blog/how-to-send-email-with-django/
            email.send()
            messages.success(
                request,
                f"Veuillez regarder votre boîte mail {user.email} pour le lien de verification. Vérifiez votre dossier spam.",
            )
                
            return render(request, "caverne/verification.html", {"messages": messages.get_messages(request)})
    else:
        form = RegisterForm()

    return render(request, "caverne/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(reverse("index"))
