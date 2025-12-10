"""
Program Model - Formation Électro
"""

from tortoise import fields

from .base import BaseModel, TimestampMixin


class Program(BaseModel, TimestampMixin):
    """
    Modèle Programme de formation
    """
    # Informations de base
    name = fields.CharField(max_length=100, description="Nom du programme", index=True)
    code = fields.CharField(max_length=50, unique=True, description="Code unique", index=True)
    description = fields.TextField(null=True, description="Description du programme")
    
    # Détails
    duration_hours = fields.IntField(default=30, description="Durée en heures")
    price = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description="Prix")
    
    # Type d'examen
    exam_type = fields.CharField(max_length=50, null=True, description="Type d'examen: emploi_quebec, cmeq, rbq, sceau_rouge")
    
    # Statut
    is_active = fields.BooleanField(default=True, description="Programme actif", index=True)
    
    # Apparence (pour le frontend)
    color = fields.CharField(max_length=20, default="#0277BC", description="Couleur hex")
    icon = fields.CharField(max_length=50, default="mdi:book-education", description="Icône MDI")
    
    # Ordre d'affichage
    display_order = fields.IntField(default=0, description="Ordre d'affichage")

    class Meta:
        table = "program"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name
