"""
Invoice API Endpoints - CRUD Operations
"""

import logging
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.invoice import invoice_controller, payment_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.invoices import InvoiceCreate, InvoiceUpdate, PaymentCreate

logger = logging.getLogger(__name__)

router = APIRouter()


def serialize_invoice(obj: dict) -> dict:
    """Convert Decimal and date types for JSON"""
    for key in ['subtotal', 'tax_tps', 'tax_tvq', 'total', 'amount_paid']:
        if obj.get(key) is not None:
            obj[key] = float(obj[key])
    for key in ['issue_date', 'due_date', 'paid_date']:
        if obj.get(key) is not None:
            obj[key] = str(obj[key])
    return obj


@router.get("/list", summary="Liste des factures")
async def list_invoices(
    page: int = Query(1, description="Numéro de page"),
    page_size: int = Query(20, description="Éléments par page"),
    search: str = Query("", description="Recherche par numéro ou étudiant"),
    student_id: int = Query(None, description="Filtrer par étudiant"),
    status: str = Query(None, description="Filtrer par statut"),
):
    """
    Récupérer la liste des factures avec pagination.
    """
    q = Q()
    if search:
        q &= Q(invoice_number__icontains=search)
    if student_id:
        q &= Q(student_id=student_id)
    if status:
        q &= Q(status=status)
    
    total, invoice_objs = await invoice_controller.list(
        page=page,
        page_size=page_size,
        search=q,
        order=["-created_at"]
    )
    
    data = []
    for obj in invoice_objs:
        await obj.fetch_related("student", "session")
        d = await obj.to_dict()
        d = serialize_invoice(d)
        d['balance_due'] = float(obj.total - obj.amount_paid)
        if obj.student:
            d['student_name'] = f"{obj.student.first_name} {obj.student.last_name}"
            d['student_email'] = obj.student.email
        if obj.session:
            d['session_title'] = obj.session.title
        data.append(d)
    
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="Détail d'une facture")
async def get_invoice(
    invoice_id: int = Query(..., description="ID de la facture"),
):
    """
    Récupérer les détails d'une facture.
    """
    invoice_obj = await invoice_controller.get_with_relations(invoice_id)
    if not invoice_obj:
        return Fail(code=404, msg="Facture non trouvée")
    
    d = await invoice_obj.to_dict()
    d = serialize_invoice(d)
    d['balance_due'] = float(invoice_obj.total - invoice_obj.amount_paid)
    
    if invoice_obj.student:
        d['student_name'] = f"{invoice_obj.student.first_name} {invoice_obj.student.last_name}"
        d['student_email'] = invoice_obj.student.email
    if invoice_obj.session:
        d['session_title'] = invoice_obj.session.title
    
    return Success(data=d)


@router.post("/create", summary="Créer une facture")
async def create_invoice(invoice_in: InvoiceCreate):
    """
    Créer une nouvelle facture avec calcul automatique des taxes.
    """
    new_invoice = await invoice_controller.create_invoice(obj_in=invoice_in)
    return Success(msg="Facture créée avec succès", data={
        "id": new_invoice.id,
        "invoice_number": new_invoice.invoice_number
    })


@router.post("/update", summary="Modifier une facture")
async def update_invoice(invoice_in: InvoiceUpdate):
    """
    Mettre à jour une facture.
    """
    # If subtotal changed, recalculate taxes
    if invoice_in.subtotal is not None:
        await invoice_controller.update_invoice_totals(invoice_in.id, invoice_in.subtotal)
    
    await invoice_controller.update(id=invoice_in.id, obj_in=invoice_in)
    return Success(msg="Facture modifiée avec succès")


@router.delete("/delete", summary="Supprimer une facture")
async def delete_invoice(
    invoice_id: int = Query(..., description="ID de la facture"),
):
    """
    Supprimer une facture.
    """
    invoice = await invoice_controller.get(id=invoice_id)
    if invoice.status == "paid":
        return Fail(code=400, msg="Impossible de supprimer une facture payée")
    
    await invoice_controller.remove(id=invoice_id)
    return Success(msg="Facture supprimée avec succès")


@router.post("/send", summary="Envoyer une facture")
async def send_invoice(
    invoice_id: int = Query(..., description="ID de la facture"),
):
    """
    Marquer la facture comme envoyée.
    """
    invoice = await invoice_controller.get(id=invoice_id)
    invoice.status = "sent"
    await invoice.save()
    return Success(msg="Facture marquée comme envoyée")


@router.get("/options", summary="Options pour les formulaires")
async def get_options():
    """
    Récupérer les options pour les selects.
    """
    return Success(data={
        "statuses": [
            {"value": "draft", "label": "Brouillon"},
            {"value": "sent", "label": "Envoyée"},
            {"value": "paid", "label": "Payée"},
            {"value": "partial", "label": "Paiement partiel"},
            {"value": "overdue", "label": "En retard"},
            {"value": "cancelled", "label": "Annulée"},
        ],
        "payment_methods": [
            {"value": "cash", "label": "Comptant"},
            {"value": "check", "label": "Chèque"},
            {"value": "credit_card", "label": "Carte de crédit"},
            {"value": "debit", "label": "Débit"},
            {"value": "transfer", "label": "Virement"},
            {"value": "interac", "label": "Interac"},
        ],
        "tax_rates": {
            "tps": 5.0,
            "tvq": 9.975,
        }
    })


@router.get("/stats", summary="Statistiques de facturation")
async def get_stats():
    """
    Récupérer les statistiques de facturation.
    """
    from tortoise.functions import Sum, Count
    
    # Total invoices
    total_count = await invoice_controller.model.all().count()
    
    # By status
    paid = await invoice_controller.model.filter(status="paid").count()
    pending = await invoice_controller.model.filter(status__in=["draft", "sent"]).count()
    overdue = await invoice_controller.model.filter(status="overdue").count()
    
    # Amounts
    total_result = await invoice_controller.model.all().annotate(
        sum_total=Sum("total"),
        sum_paid=Sum("amount_paid")
    ).values("sum_total", "sum_paid")
    
    total_billed = float(total_result[0]["sum_total"] or 0) if total_result else 0
    total_collected = float(total_result[0]["sum_paid"] or 0) if total_result else 0
    
    return Success(data={
        "total_invoices": total_count,
        "paid": paid,
        "pending": pending,
        "overdue": overdue,
        "total_billed": total_billed,
        "total_collected": total_collected,
        "balance_due": total_billed - total_collected,
    })


# ==================== PAYMENTS ====================

@router.get("/payments", summary="Paiements d'une facture")
async def get_invoice_payments(
    invoice_id: int = Query(..., description="ID de la facture"),
):
    """
    Récupérer tous les paiements d'une facture.
    """
    payments = await payment_controller.get_invoice_payments(invoice_id)
    data = []
    for p in payments:
        d = await p.to_dict()
        if d.get('amount') is not None:
            d['amount'] = float(d['amount'])
        if d.get('payment_date'):
            d['payment_date'] = str(d['payment_date'])
        data.append(d)
    
    return Success(data=data)


@router.post("/payment", summary="Enregistrer un paiement")
async def add_payment(payment_in: PaymentCreate):
    """
    Enregistrer un paiement sur une facture.
    """
    # Validate amount
    invoice = await invoice_controller.get(id=payment_in.invoice_id)
    balance = invoice.total - invoice.amount_paid
    
    if payment_in.amount > balance:
        return Fail(code=400, msg=f"Le montant dépasse le solde dû ({float(balance):.2f}$)")
    
    payment = await payment_controller.add_payment(obj_in=payment_in)
    return Success(msg="Paiement enregistré avec succès", data={"id": payment.id})


@router.delete("/payment/delete", summary="Supprimer un paiement")
async def delete_payment(
    payment_id: int = Query(..., description="ID du paiement"),
):
    """
    Supprimer un paiement.
    """
    from app.models.invoice import Payment, Invoice
    
    payment = await Payment.get(id=payment_id)
    invoice = await Invoice.get(id=payment.invoice_id)
    
    # Update invoice
    invoice.amount_paid -= payment.amount
    if invoice.amount_paid <= 0:
        invoice.status = "sent"
        invoice.paid_date = None
    elif invoice.amount_paid < invoice.total:
        invoice.status = "partial"
    await invoice.save()
    
    await payment.delete()
    return Success(msg="Paiement supprimé")
