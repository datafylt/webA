"""
Invoice Schemas - Pydantic models for validation
"""

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class InvoiceCreate(BaseModel):
    """Schema pour créer une facture"""

    student_id: int = Field(..., description="ID de l'étudiant")
    session_id: Optional[int] = Field(None, description="ID de la session")
    subtotal: Decimal = Field(..., ge=0, description="Sous-total")
    description: Optional[str] = Field(None, description="Description")
    due_date: Optional[date] = Field(None, description="Date d'échéance")


class InvoiceUpdate(BaseModel):
    """Schema pour mettre à jour une facture"""

    id: int = Field(..., description="ID de la facture")
    subtotal: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class PaymentCreate(BaseModel):
    """Schema pour enregistrer un paiement"""

    invoice_id: int = Field(..., description="ID de la facture")
    amount: Decimal = Field(..., gt=0, description="Montant")
    payment_method: str = Field(..., description="Méthode de paiement")
    reference: Optional[str] = Field(None, description="Référence")
    notes: Optional[str] = Field(None, description="Notes")


# Choix
INVOICE_STATUS_CHOICES = [
    ("draft", "Brouillon"),
    ("sent", "Envoyée"),
    ("paid", "Payée"),
    ("partial", "Paiement partiel"),
    ("overdue", "En retard"),
    ("cancelled", "Annulée"),
]

PAYMENT_METHOD_CHOICES = [
    ("cash", "Comptant"),
    ("check", "Chèque"),
    ("credit_card", "Carte de crédit"),
    ("debit", "Débit"),
    ("transfer", "Virement"),
    ("interac", "Interac"),
]
