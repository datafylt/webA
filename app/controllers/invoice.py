"""
Invoice Controller - Business logic for Invoice CRUD
"""

from datetime import date
from decimal import Decimal
from typing import Optional

from app.core.crud import CRUDBase
from app.models.invoice import Invoice, Payment
from app.schemas.invoices import InvoiceCreate, InvoiceUpdate, PaymentCreate


# Taux de taxes Québec
TPS_RATE = Decimal("0.05")
TVQ_RATE = Decimal("0.09975")


class InvoiceController(CRUDBase[Invoice, InvoiceCreate, InvoiceUpdate]):
    def __init__(self):
        super().__init__(model=Invoice)

    async def generate_invoice_number(self) -> str:
        """Generate unique invoice number: FE-YYYYMM-XXXX"""
        today = date.today()
        prefix = f"FE-{today.strftime('%Y%m')}-"
        
        # Find last invoice number for this month
        last_invoice = await self.model.filter(
            invoice_number__startswith=prefix
        ).order_by("-invoice_number").first()
        
        if last_invoice:
            last_num = int(last_invoice.invoice_number.split("-")[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        return f"{prefix}{new_num:04d}"

    async def create_invoice(self, obj_in: InvoiceCreate) -> Invoice:
        """Create invoice with calculated taxes"""
        invoice_number = await self.generate_invoice_number()
        
        subtotal = obj_in.subtotal
        tax_tps = subtotal * TPS_RATE
        tax_tvq = subtotal * TVQ_RATE
        total = subtotal + tax_tps + tax_tvq
        
        invoice = await self.model.create(
            invoice_number=invoice_number,
            student_id=obj_in.student_id,
            session_id=obj_in.session_id,
            subtotal=subtotal,
            tax_tps=tax_tps.quantize(Decimal("0.01")),
            tax_tvq=tax_tvq.quantize(Decimal("0.01")),
            total=total.quantize(Decimal("0.01")),
            description=obj_in.description,
            due_date=obj_in.due_date,
            status="draft",
        )
        return invoice

    async def update_invoice_totals(self, invoice_id: int, subtotal: Decimal):
        """Recalculate taxes when subtotal changes"""
        invoice = await self.get(id=invoice_id)
        
        tax_tps = subtotal * TPS_RATE
        tax_tvq = subtotal * TVQ_RATE
        total = subtotal + tax_tps + tax_tvq
        
        invoice.subtotal = subtotal
        invoice.tax_tps = tax_tps.quantize(Decimal("0.01"))
        invoice.tax_tvq = tax_tvq.quantize(Decimal("0.01"))
        invoice.total = total.quantize(Decimal("0.01"))
        
        await invoice.save()
        return invoice

    async def get_with_relations(self, id: int) -> Optional[Invoice]:
        """Get invoice with student and session"""
        return await self.model.filter(id=id).prefetch_related("student", "session").first()

    async def update_payment_status(self, invoice_id: int):
        """Update invoice status based on payments"""
        invoice = await self.get(id=invoice_id)
        
        if invoice.amount_paid >= invoice.total:
            invoice.status = "paid"
            invoice.paid_date = date.today()
        elif invoice.amount_paid > 0:
            invoice.status = "partial"
        
        await invoice.save()
        return invoice


class PaymentController(CRUDBase[Payment, PaymentCreate, PaymentCreate]):
    def __init__(self):
        super().__init__(model=Payment)

    async def add_payment(self, obj_in: PaymentCreate) -> Payment:
        """Add payment and update invoice"""
        payment = await self.model.create(
            invoice_id=obj_in.invoice_id,
            amount=obj_in.amount,
            payment_method=obj_in.payment_method,
            reference=obj_in.reference,
            notes=obj_in.notes,
        )
        
        # Update invoice amount_paid
        invoice = await Invoice.get(id=obj_in.invoice_id)
        invoice.amount_paid += obj_in.amount
        invoice.payment_method = obj_in.payment_method
        await invoice.save()
        
        # Update invoice status
        await invoice_controller.update_payment_status(obj_in.invoice_id)
        
        return payment

    async def get_invoice_payments(self, invoice_id: int):
        """Get all payments for an invoice"""
        return await self.model.filter(invoice_id=invoice_id).order_by("-payment_date")


invoice_controller = InvoiceController()
payment_controller = PaymentController()
