"""
Instructor Model - Formation Électro
"""

from tortoise import fields

from .base import BaseModel, TimestampMixin


class Instructor(BaseModel, TimestampMixin):
    """
    Modèle Formateur
    """

    # Informations personnelles
    first_name = fields.CharField(max_length=100, description="Prénom")
    last_name = fields.CharField(max_length=100, description="Nom")
    email = fields.CharField(max_length=255, unique=True, index=True, description="Email")
    phone = fields.CharField(max_length=20, null=True, description="Téléphone")

    # Informations professionnelles
    specialization = fields.CharField(max_length=100, null=True, description="Spécialisation")
    bio = fields.TextField(null=True, description="Biographie")
    certifications = fields.TextField(null=True, description="Certifications (séparées par virgules)")
    years_experience = fields.IntField(default=0, description="Années d'expérience")

    # Disponibilité et tarification
    hourly_rate = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="Taux horaire")
    is_available = fields.BooleanField(default=True, description="Disponible")

    # Statut
    status = fields.CharField(
        max_length=20, default="active", index=True, description="Statut: active, inactive, on_leave"
    )

    # Photo
    photo_url = fields.CharField(max_length=500, null=True, description="URL photo")

    # Notes internes
    notes = fields.TextField(null=True, description="Notes internes")

    class Meta:
        table = "instructor"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
