from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q, Value
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .decorators import unauth_required, verified_required
from .forms import FichierForm, RegisterForm
from .helper import ArrayToString, VerificationEmail, account_activation_token
from .models import Enseignant, Fichier


@login_required
@verified_required
def index(request):
    return render(request, "caverne/index.html")

@login_required
@verified_required
def search_autocomplete(request):
    search_text = request.POST.get("search")

    context = {}
    if not search_text.isspace() and search_text:
        q_name = q_tags = q_description = Q()
        for word in search_text.split():
            q_name |= Q(name__unaccent__icontains=word) | Q(
                name__trigram_word_similar=word
            )
            q_tags |= Q(tags_text__unaccent__icontains=word) | Q(tags_text__trigram_word_similar=word)
            q_description |= Q(description__unaccent__icontains=word) | Q(
                description__trigram_word_similar=word
            )
            
        results = Fichier.objects.annotate(tags_text=ArrayToString("tags", Value(" "))).filter(q_name | q_tags | q_description).distinct()[:5]
        context["results"] = results
        
    return render(request, "caverne/partials/search_autocomplete.html", context)

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

@unauth_required
def send_verification(request, user):
    User = get_user_model()
    context = {}
    
    if isinstance(user, str):
        try:
            uid = force_str(urlsafe_base64_decode(user))
            u = User.objects.get(pk=uid)
        except (TypeError, OverflowError, ValueError, User.DoesNotExist):
            u = None
    else:
        u = user
        
    if u is None:
        return HttpResponse("Ce compte n'existe pas!", status=404)
    
    if u.verified:
        status = 1
        context["status"] = status
    else:
        email = VerificationEmail(
                    u,
                    "Vérifiez votre compte",
                    reply_to=["no-reply@caverne.ch"],
                )
        email.make_body(
            get_current_site(request).domain, is_secure=request.is_secure()
        )
        email.send()
        
        messages.success(
                    request,
                    f"Veuillez regarder votre boîte mail {u.email} pour le lien de verification. Vérifiez votre dossier spam.",
                )
        
        context["messages"] = messages.get_messages(request)
    
    return render(request, "caverne/verification.html", context)

@unauth_required
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return send_verification(request, user)

    else:
        form = RegisterForm()

    return render(request, "caverne/register.html", {"form": form})

def activate(request, uidb64, token):
    User = get_user_model()
    context = {}
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, OverflowError, ValueError, User.DoesNotExist):
        user = None

    is_verified, is_expired = account_activation_token.check_token(user, token)
    if is_verified:
        user.verified = True
        user.save()

        login(request, user)
        status = 1
    elif is_expired:
        # Pour permettre à l'utilisateur de recevoir un autre lien
        link = {
            "protocol": "https" if request.is_secure()  else "http",
            "domain": get_current_site(request).domain,
            "uid": uidb64,
        }
        context["link"] = link
        status = 2
    else:
        status = 3
    
    context["status"] = status
    return render(request, "caverne/verification.html", context)

def logout_view(request):
    logout(request)
    return redirect(reverse("index"))
