"""
Student Schemas - Pydantic models for validation
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    """Schema pour créer un étudiant"""
    first_name: str = Field(..., min_length=1, max_length=50, description="Prénom")
    last_name: str = Field(..., min_length=1, max_length=50, description="Nom")
    email: EmailStr = Field(..., description="Email")
    phone: Optional[str] = Field(None, max_length=20, description="Téléphone")
    address: Optional[str] = Field(None, max_length=255, description="Adresse")
    city: Optional[str] = Field(None, max_length=100, description="Ville")
    postal_code: Optional[str] = Field(None, max_length=10, description="Code postal")
    employer: Optional[str] = Field(None, max_length=100, description="Employeur")
    ccq_number: Optional[str] = Field(None, max_length=50, description="No. Carte CCQ")
    apprentice_hours: int = Field(default=0, ge=0, description="Heures d'apprentissage")
    goal: Optional[str] = Field(None, description="Programme visé")
    notes: Optional[str] = Field(None, description="Notes internes")


class StudentUpdate(BaseModel):
    """Schema pour mettre à jour un étudiant (tous les champs optionnels)"""
    id: int = Field(..., description="ID de l'étudiant")
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=10)
    employer: Optional[str] = Field(None, max_length=100)
    ccq_number: Optional[str] = Field(None, max_length=50)
    apprentice_hours: Optional[int] = Field(None, ge=0)
    goal: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive|expired)$")
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None


# Choix pour le champ 'goal'
GOAL_CHOICES = [
    ("licence_c", "Licence C - Compagnon Électricien"),
    ("rca", "RCA - Connexions Restreintes"),
    ("rbq", "RBQ - Constructeur Propriétaire"),
    ("cmeq", "CMEQ - Entrepreneur Électricien"),
    ("sceau_rouge", "Sceau Rouge - Interprovincial"),
    ("custom", "Formation sur mesure"),
]

# Choix pour le champ 'status'
STATUS_CHOICES = [
    ("active", "Actif"),
    ("inactive", "Inactif"),
    ("expired", "Expiré"),
]
