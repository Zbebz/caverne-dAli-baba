from pathlib import Path
from uuid import uuid4
import magic

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import localtime
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

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

TYPES = [
    ("EVAL", "Évaluation"),
    ("THEO", "Théorie"),
    ("EXOS", "Exercices"),
]

YEARS = [(1, "1re"), (2, "2e"), (3, "3e"), (4, "4e")]

STATUTS = [(2, "En attente"), (0, "Rejeté"), (1, "Chargé")]


class User(AbstractUser):
    username = models.CharField(
        unique=True, blank=False, null=False, verbose_name="identifiant eduge"
    )
    ecole = models.CharField(
        blank=False,
        null=False,
        choices=ECOLES,
        verbose_name="collège",
    )
    email = models.EmailField(blank=True, null=False)

    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):
        self.email = f"{self.username}@eduge.ch"
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.get_ecole_display()}"


class Enseignant(models.Model):
    name = models.CharField(
        blank=False, null=False, max_length=50, unique=True, verbose_name="nom, prénom"
    )
    ecole = models.CharField(
        blank=False, null=False, choices=ECOLES, verbose_name="collège"
    )

    def __str__(self):
        return f"{self.name} - {self.get_ecole_display()}"


def filePlacer(instance, filename):
    return f"{Path(filename).suffix[1:]}/{filename}"


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


def validate_file_mimetype(file):
    accept = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.oasis.opendocument.text",
    ]
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)
    print(file_mime_type)
    if file_mime_type not in accept:
        raise ValidationError("Ce type de fichier n'est pas autorisé.")


class Fichier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="fichiers",
    )
    status = models.IntegerField(default=2, choices=STATUTS)
    uploadDatetime = models.DateTimeField(default=localtime)

    file = models.FileField(
        upload_to=filePlacer,
        verbose_name="fichier",
        null=False,
        blank=False,
        validators=[
            FileExtensionValidator(["pdf", "doc", "docx", "odt"]),
            validate_file_mimetype,
        ],
    )
    name = models.CharField(blank=False, null=False, verbose_name="nom du fichier")
    year = models.IntegerField(
        blank=False, null=False, choices=YEARS, verbose_name="année"
    )  # L'année pour laquelle le fichier est destiné
    subject = models.CharField(
        blank=False, null=False, choices=SUBJECTS, verbose_name="matière"
    )
    type = models.CharField(
        blank=False, null=False, choices=TYPES, verbose_name="type de fichier"
    )
    ecole = models.CharField(
        blank=False, null=False, choices=ECOLES, verbose_name="collège"
    )
    enseignant = models.CharField(blank=False, null=False, verbose_name="enseignant.e")
    annotated = models.BooleanField(blank=False, null=False, verbose_name="annoté?")
    description = models.TextField(blank=False, null=False)
    tags = models.TextField(blank=False, null=False, verbose_name="mots clés")

    def __str__(self):
        return f"{self.name} - {self.user.username}"
