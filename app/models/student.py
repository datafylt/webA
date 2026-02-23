"""
Student Model - Formation Électro
"""

from tortoise import fields

from .base import BaseModel, TimestampMixin


class Student(BaseModel, TimestampMixin):
    """
    Modèle Étudiant pour Formation Électro
    """

    # Informations personnelles
    first_name = fields.CharField(max_length=50, description="Prénom", index=True)
    last_name = fields.CharField(max_length=50, description="Nom de famille", index=True)
    email = fields.CharField(max_length=255, unique=True, description="Email", index=True)
    phone = fields.CharField(max_length=20, null=True, description="Téléphone")

    # Adresse
    address = fields.CharField(max_length=255, null=True, description="Adresse")
    city = fields.CharField(max_length=100, null=True, description="Ville")
    postal_code = fields.CharField(max_length=10, null=True, description="Code postal")

    # Informations professionnelles
    employer = fields.CharField(max_length=100, null=True, description="Employeur")
    ccq_number = fields.CharField(max_length=50, null=True, description="No. Carte CCQ")
    apprentice_hours = fields.IntField(default=0, description="Heures d'apprentissage")

    # Programme visé
    goal = fields.CharField(max_length=50, null=True, description="Objectif/Programme visé", index=True)

    # Statut: active, inactive, expired
    status = fields.CharField(max_length=20, default="active", description="Statut", index=True)

    # Notes internes (admin seulement)
    notes = fields.TextField(null=True, description="Notes internes")

    # Date d'expiration accès
    expires_at = fields.DatetimeField(null=True, description="Date d'expiration accès")

    class Meta:
        table = "student"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
