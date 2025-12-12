"""
Notification Schemas - Pydantic models for validation
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr


class TemplateCreate(BaseModel):
    """Schema pour créer un template"""
    name: str = Field(..., min_length=1, max_length=100, description="Nom du template")
    subject: str = Field(..., min_length=1, max_length=255, description="Sujet")
    body: str = Field(..., description="Corps du message")
    notification_type: str = Field("general", description="Type de notification")
    variables: Optional[str] = Field(None, description="Variables disponibles")
    is_active: bool = Field(True, description="Actif")


class TemplateUpdate(BaseModel):
    """Schema pour mettre à jour un template"""
    id: int = Field(..., description="ID du template")
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    notification_type: Optional[str] = None
    variables: Optional[str] = None
    is_active: Optional[bool] = None


class NotificationCreate(BaseModel):
    """Schema pour créer une notification"""
    recipient_email: EmailStr = Field(..., description="Email destinataire")
    recipient_name: Optional[str] = Field(None, description="Nom destinataire")
    student_id: Optional[int] = Field(None, description="ID étudiant")
    subject: str = Field(..., min_length=1, max_length=255, description="Sujet")
    body: str = Field(..., description="Corps du message")
    notification_type: str = Field("general", description="Type")
    template_id: Optional[int] = Field(None, description="ID template")
    scheduled_at: Optional[datetime] = Field(None, description="Date d'envoi programmé")


class BulkNotificationCreate(BaseModel):
    """Schema pour envoi en masse"""
    recipient_ids: List[int] = Field(..., description="Liste des IDs étudiants")
    subject: str = Field(..., min_length=1, max_length=255, description="Sujet")
    body: str = Field(..., description="Corps du message")
    notification_type: str = Field("general", description="Type")
    template_id: Optional[int] = Field(None, description="ID template")


# Choix
NOTIFICATION_TYPE_CHOICES = [
    ("general", "Général"),
    ("reminder", "Rappel"),
    ("confirmation", "Confirmation"),
    ("invoice", "Facture"),
    ("welcome", "Bienvenue"),
    ("session", "Session"),
]

STATUS_CHOICES = [
    ("pending", "En attente"),
    ("sent", "Envoyé"),
    ("failed", "Échec"),
    ("cancelled", "Annulé"),
]
