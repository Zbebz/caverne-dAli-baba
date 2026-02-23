from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

ECOLES = [
    ("CHAVANNE", "Collège et Ecole de commerce André-Chavanne"),
    ("CALVIN", "Collège Calvin"),
    ("CLAPAREDE", "Collège Claparède"),
    ("CANDOLLE", "Collège de Candolle"),
    ("SAUSSURE", "Collège de Saussure"),
    ("EMILIE", "Collège Emilie-Gourd"),
    ("STAEL", "Collège Madame de Staël"),
    ("RIVAZ", "Collège pour adultes Alice-Rivaz"),
    ("ROUSSEAU", "Collège Rousseau"),
    ("SISMONDI", "Collège Sismondi"),
    ("VOLTAIRE", "Collège Voltaire"),
]


class User(AbstractUser):
    username = models.CharField(
        unique=True, blank=False, null=False, verbose_name="identifiant eduge"
    )
    ecole = models.CharField(
        blank=False,
        null=False,
        choices=ECOLES,
        verbose_name="établissement scolaire",
    )
    email = models.EmailField()

    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):
        self.email = f"{self.username}@eduge.ch"
        self.first_name, self.last_name = self.username.split(".")
        return super().save(*args, **kwargs)
