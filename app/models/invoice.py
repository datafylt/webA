"""
Invoice Model - Formation Électro
"""

from tortoise import fields

from .base import BaseModel, TimestampMixin


class Invoice(BaseModel, TimestampMixin):
    """
    Modèle Facture
    """

    # Numéro de facture unique
    invoice_number = fields.CharField(max_length=50, unique=True, index=True, description="Numéro de facture")

    # Relations
    student = fields.ForeignKeyField(
        "models.Student", related_name="invoices", on_delete=fields.CASCADE, description="Étudiant facturé"
    )
    session = fields.ForeignKeyField(
        "models.Session",
        related_name="invoices",
        on_delete=fields.SET_NULL,
        null=True,
        description="Session associée (optionnel)",
    )

    # Montants
    subtotal = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description="Sous-total")
    tax_tps = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description="TPS (5%)")
    tax_tvq = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description="TVQ (9.975%)")
    total = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description="Total")
    amount_paid = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description="Montant payé")

    # Statut
    status = fields.CharField(
        max_length=20, default="draft", index=True, description="Statut: draft, sent, paid, partial, overdue, cancelled"
    )

    # Dates
    issue_date = fields.DateField(auto_now_add=True, description="Date d'émission")
    due_date = fields.DateField(null=True, description="Date d'échéance")
    paid_date = fields.DateField(null=True, description="Date de paiement")

    # Description
    description = fields.TextField(null=True, description="Description/notes")

    # Méthode de paiement
    payment_method = fields.CharField(
        max_length=50, null=True, description="Méthode: cash, check, credit_card, transfer, interac"
    )

    class Meta:
        table = "invoice"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Facture {self.invoice_number}"

    @property
    def balance_due(self):
        return self.total - self.amount_paid


class Payment(BaseModel, TimestampMixin):
    """
    Modèle Paiement (historique des paiements sur une facture)
    """

    invoice = fields.ForeignKeyField("models.Invoice", related_name="payments", on_delete=fields.CASCADE)

    amount = fields.DecimalField(max_digits=10, decimal_places=2, description="Montant payé")
    payment_date = fields.DateField(auto_now_add=True, description="Date du paiement")
    payment_method = fields.CharField(max_length=50, description="Méthode de paiement")
    reference = fields.CharField(max_length=100, null=True, description="Référence/numéro chèque")
    notes = fields.TextField(null=True, description="Notes")

    class Meta:
        table = "payment"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Paiement {self.amount} - {self.payment_date}"
