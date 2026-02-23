"""
Session Schemas - Pydantic models for validation
"""

from datetime import date, time
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Schema pour créer une session"""

    program_id: int = Field(..., description="ID du programme")
    title: str = Field(..., min_length=1, max_length=200, description="Titre")
    description: Optional[str] = Field(None, description="Description")
    start_date: date = Field(..., description="Date de début")
    end_date: Optional[date] = Field(None, description="Date de fin")
    start_time: Optional[time] = Field(None, description="Heure de début")
    end_time: Optional[time] = Field(None, description="Heure de fin")
    location_type: str = Field(default="in_person", description="Type de lieu")
    location: Optional[str] = Field(None, description="Lieu physique")
    online_link: Optional[str] = Field(None, description="Lien en ligne")
    max_participants: int = Field(default=15, ge=1, description="Places max")
    min_participants: int = Field(default=1, ge=1, description="Places min")
    price: Optional[Decimal] = Field(None, ge=0, description="Prix")
    status: str = Field(default="scheduled", description="Statut")
    instructor_name: Optional[str] = Field(None, description="Formateur")


class SessionUpdate(BaseModel):
    """Schema pour mettre à jour une session"""

    id: int = Field(..., description="ID de la session")
    program_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location_type: Optional[str] = None
    location: Optional[str] = None
    online_link: Optional[str] = None
    max_participants: Optional[int] = Field(None, ge=1)
    min_participants: Optional[int] = Field(None, ge=1)
    price: Optional[Decimal] = Field(None, ge=0)
    status: Optional[str] = None
    instructor_name: Optional[str] = None


class EnrollmentCreate(BaseModel):
    """Schema pour inscrire un étudiant"""

    session_id: int = Field(..., description="ID de la session")
    student_id: int = Field(..., description="ID de l'étudiant")
    notes: Optional[str] = None


class EnrollmentUpdate(BaseModel):
    """Schema pour modifier une inscription"""

    id: int = Field(..., description="ID de l'inscription")
    status: Optional[str] = None
    payment_status: Optional[str] = None
    amount_paid: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


# Choix
LOCATION_TYPE_CHOICES = [
    ("in_person", "En personne"),
    ("online", "En ligne"),
    ("hybrid", "Hybride"),
]

SESSION_STATUS_CHOICES = [
    ("scheduled", "Planifiée"),
    ("in_progress", "En cours"),
    ("completed", "Terminée"),
    ("cancelled", "Annulée"),
]

ENROLLMENT_STATUS_CHOICES = [
    ("enrolled", "Inscrit"),
    ("completed", "Complété"),
    ("cancelled", "Annulé"),
    ("no_show", "Absent"),
]

PAYMENT_STATUS_CHOICES = [
    ("pending", "En attente"),
    ("paid", "Payé"),
    ("refunded", "Remboursé"),
]
