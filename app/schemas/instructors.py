"""
Instructor Schemas - Pydantic models for validation
"""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class InstructorCreate(BaseModel):
    """Schema pour créer un formateur"""

    first_name: str = Field(..., min_length=1, max_length=100, description="Prénom")
    last_name: str = Field(..., min_length=1, max_length=100, description="Nom")
    email: EmailStr = Field(..., description="Email")
    phone: Optional[str] = Field(None, max_length=20, description="Téléphone")
    specialization: Optional[str] = Field(None, max_length=100, description="Spécialisation")
    bio: Optional[str] = Field(None, description="Biographie")
    certifications: Optional[str] = Field(None, description="Certifications")
    years_experience: int = Field(0, ge=0, description="Années d'expérience")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="Taux horaire")
    is_available: bool = Field(True, description="Disponible")
    photo_url: Optional[str] = Field(None, description="URL photo")
    notes: Optional[str] = Field(None, description="Notes")


class InstructorUpdate(BaseModel):
    """Schema pour mettre à jour un formateur"""

    id: int = Field(..., description="ID du formateur")
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    bio: Optional[str] = None
    certifications: Optional[str] = None
    years_experience: Optional[int] = None
    hourly_rate: Optional[Decimal] = None
    is_available: Optional[bool] = None
    status: Optional[str] = None
    photo_url: Optional[str] = None
    notes: Optional[str] = None


# Choix
STATUS_CHOICES = [
    ("active", "Actif"),
    ("inactive", "Inactif"),
    ("on_leave", "En congé"),
]

SPECIALIZATION_CHOICES = [
    ("licence_c", "Licence C - Compagnon"),
    ("rca", "RCA - Connexions Restreintes"),
    ("rbq", "RBQ - Constructeur Propriétaire"),
    ("cmeq", "CMEQ - Entrepreneur"),
    ("sceau_rouge", "Sceau Rouge"),
    ("code", "Code de construction"),
    ("securite", "Sécurité électrique"),
    ("general", "Formation générale"),
]
