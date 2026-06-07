from django.contrib.auth import views as auth_views
from django.urls import path

from . import views, forms

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload, name="upload"),
    path("register", views.register, name="register"),
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="caverne/login.html", authentication_form=forms.LoginForm
        ),
        name="login",
    ),
    path("logout", views.logout_view, name="logout"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    path(
        "send_verification/<str:user>/",
        views.send_verification,
        name="send_verification",
    ),
    path("search", views.SearchView.as_view(), name="search")
]

htmx_urlpatterns = [
    path("search-autocomplete", views.search_autocomplete, name="search-autocomplete"),
]

urlpatterns += htmx_urlpatterns
