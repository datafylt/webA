"""
Dashboard API Endpoints - Statistics and Overview
"""

import logging
from datetime import datetime, timedelta

from fastapi import APIRouter
from tortoise.functions import Sum, Count

from app.models.student import Student
from app.models.program import Program
from app.models.session import Session, SessionEnrollment
from app.models.invoice import Invoice
from app.models.instructor import Instructor
from app.models.notification import Notification
from app.schemas.base import Success

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/stats", summary="Statistiques du tableau de bord")
async def get_dashboard_stats():
    """
    Récupérer toutes les statistiques pour le tableau de bord.
    """
    # Students stats
    total_students = await Student.all().count()
    active_students = await Student.filter(status="active").count()
    
    # Programs stats
    total_programs = await Program.all().count()
    active_programs = await Program.filter(is_active=True).count()
    
    # Sessions stats
    total_sessions = await Session.all().count()
    upcoming_sessions = await Session.filter(
        start_date__gte=datetime.now().date(),
        status="scheduled"
    ).count()
    
    # Enrollments
    total_enrollments = await SessionEnrollment.all().count()
    
    # Invoices stats
    invoice_stats = await Invoice.all().annotate(
        sum_total=Sum("total"),
        sum_paid=Sum("amount_paid")
    ).values("sum_total", "sum_paid")
    
    total_revenue = float(invoice_stats[0]["sum_total"] or 0) if invoice_stats else 0
    total_collected = float(invoice_stats[0]["sum_paid"] or 0) if invoice_stats else 0
    
    pending_invoices = await Invoice.filter(status__in=["draft", "sent", "partial"]).count()
    
    # Instructors stats
    total_instructors = await Instructor.all().count()
    available_instructors = await Instructor.filter(status="active", is_available=True).count()
    
    # Notifications stats
    pending_notifications = await Notification.filter(status="pending").count()
    
    # Recent activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    new_students_week = await Student.filter(created_at__gte=week_ago).count()
    new_enrollments_week = await SessionEnrollment.filter(created_at__gte=week_ago).count()
    
    return Success(data={
        "students": {
            "total": total_students,
            "active": active_students,
            "new_this_week": new_students_week,
        },
        "programs": {
            "total": total_programs,
            "active": active_programs,
        },
        "sessions": {
            "total": total_sessions,
            "upcoming": upcoming_sessions,
        },
        "enrollments": {
            "total": total_enrollments,
            "new_this_week": new_enrollments_week,
        },
        "revenue": {
            "total_billed": total_revenue,
            "total_collected": total_collected,
            "pending": total_revenue - total_collected,
            "pending_invoices": pending_invoices,
        },
        "instructors": {
            "total": total_instructors,
            "available": available_instructors,
        },
        "notifications": {
            "pending": pending_notifications,
        },
    })


@router.get("/upcoming-sessions", summary="Prochaines sessions")
async def get_upcoming_sessions():
    """
    Récupérer les 5 prochaines sessions.
    """
    sessions = await Session.filter(
        start_date__gte=datetime.now().date(),
        status="scheduled"
    ).prefetch_related("program").order_by("start_date").limit(5)
    
    data = []
    for s in sessions:
        enrolled_count = await SessionEnrollment.filter(session_id=s.id, status="enrolled").count()
        data.append({
            "id": s.id,
            "title": s.title,
            "program_name": s.program.name if s.program else None,
            "start_date": str(s.start_date),
            "location_type": s.location_type,
            "enrolled": enrolled_count,
            "max_participants": s.max_participants,
        })
    
    return Success(data=data)


@router.get("/recent-students", summary="Étudiants récents")
async def get_recent_students():
    """
    Récupérer les 5 derniers étudiants inscrits.
    """
    students = await Student.all().order_by("-created_at").limit(5)
    
    data = []
    for s in students:
        data.append({
            "id": s.id,
            "full_name": s.full_name,
            "email": s.email,
            "goal": s.goal,
            "created_at": str(s.created_at),
        })
    
    return Success(data=data)


@router.get("/pending-payments", summary="Paiements en attente")
async def get_pending_payments():
    """
    Récupérer les factures en attente de paiement.
    """
    invoices = await Invoice.filter(
        status__in=["sent", "partial", "overdue"]
    ).prefetch_related("student").order_by("-created_at").limit(5)
    
    data = []
    for inv in invoices:
        data.append({
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "student_name": inv.student.full_name if inv.student else None,
            "total": float(inv.total),
            "amount_paid": float(inv.amount_paid),
            "balance_due": float(inv.total - inv.amount_paid),
            "status": inv.status,
        })
    
    return Success(data=data)
