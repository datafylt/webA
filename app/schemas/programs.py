"""
Program Schemas - Pydantic models for validation
"""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ProgramCreate(BaseModel):
    """Schema pour créer un programme"""
    name: str = Field(..., min_length=1, max_length=100, description="Nom du programme")
    code: str = Field(..., min_length=1, max_length=50, description="Code unique")
    description: Optional[str] = Field(None, description="Description")
    duration_hours: int = Field(default=30, ge=0, description="Durée en heures")
    price: Decimal = Field(default=Decimal("0"), ge=0, description="Prix")
    exam_type: Optional[str] = Field(None, description="Type d'examen")
    is_active: bool = Field(default=True, description="Programme actif")
    color: str = Field(default="#0277BC", description="Couleur hex")
    icon: str = Field(default="mdi:book-education", description="Icône MDI")
    display_order: int = Field(default=0, description="Ordre d'affichage")


class ProgramUpdate(BaseModel):
    """Schema pour mettre à jour un programme"""
    id: int = Field(..., description="ID du programme")
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    duration_hours: Optional[int] = Field(None, ge=0)
    price: Optional[Decimal] = Field(None, ge=0)
    exam_type: Optional[str] = None
    is_active: Optional[bool] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    display_order: Optional[int] = None


# Choix pour exam_type
EXAM_TYPE_CHOICES = [
    ("emploi_quebec", "Emploi-Québec"),
    ("cmeq", "CMEQ"),
    ("rbq", "RBQ"),
    ("sceau_rouge", "Sceau Rouge (Interprovincial)"),
]
