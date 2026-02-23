from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
import uuid
from pathlib import Path

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

SUBJECTS = [
    ("AN", "Anglais"),
    ("BI", "Biologie"),
    ("FR", "Français"),
    ("GE", "Géographie"),
    ("HI", "Histoire"),
    ("IT", "Italien"),
    ("MA", "Mathématiques"),
    ("PY", "Physique"),
    ("AM", "Applications des maths"),
    ("PO", "Philosophie"),
]

YEARS = [(1, "1re"), (2, "2e"), (3, "3e"), (4, "4e")]


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
    email = models.EmailField(blank=False, null=False)

    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):
        self.email = f"{self.username}@eduge.ch"
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.get_ecole_display()}"


def filePlacer(instance, filename):
    return f"{Path(filename).suffix[1:]}/{filename}"


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Fichier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="fichiers",
    )
    name = models.CharField(blank=False, null=False, verbose_name="nom du fichier")
    description = models.TextField(blank=False, null=False)
    year = models.IntegerField(
        blank=False, null=False, choices=YEARS, verbose_name="années"
    ) # L'année pour laquelle le fichier est destiné
    subject = models.CharField(
        blank=False, null=False, choices=SUBJECTS, verbose_name="matière"
    )
    status = models.CharField(blank=False, null=False, default="PENDING")
    tags = models.TextField(blank=False, null=False, verbose_name="mots clés")
    uploadDatetime = models.DateTimeField(default=localtime)

    file = models.FileField(
        upload_to=filePlacer, verbose_name="fichier", null=False, blank=False
    )
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    # def save(self, *args, **kwargs):
    #     self.file = None
    #     return super().save(*args, **kwargs)
