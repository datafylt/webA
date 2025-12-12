"""
Notification API Endpoints - CRUD Operations
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.notification import notification_controller, template_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.notifications import NotificationCreate, BulkNotificationCreate, TemplateCreate, TemplateUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


# ==================== TEMPLATES ====================

@router.get("/templates", summary="Liste des templates")
async def list_templates(
    page: int = Query(1, description="Numéro de page"),
    page_size: int = Query(20, description="Éléments par page"),
    notification_type: str = Query(None, description="Filtrer par type"),
):
    """
    Récupérer la liste des templates.
    """
    q = Q()
    if notification_type:
        q &= Q(notification_type=notification_type)
    
    total, template_objs = await template_controller.list(
        page=page,
        page_size=page_size,
        search=q,
        order=["name"]
    )
    
    data = [await obj.to_dict() for obj in template_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/templates/active", summary="Templates actifs")
async def get_active_templates():
    """
    Récupérer tous les templates actifs pour les selects.
    """
    templates = await template_controller.get_active_templates()
    data = [{"id": t.id, "name": t.name, "subject": t.subject, "type": t.notification_type} for t in templates]
    return Success(data=data)


@router.get("/template/get", summary="Détail d'un template")
async def get_template(
    template_id: int = Query(..., description="ID du template"),
):
    """
    Récupérer les détails d'un template.
    """
    template_obj = await template_controller.get(id=template_id)
    if not template_obj:
        return Fail(code=404, msg="Template non trouvé")
    
    return Success(data=await template_obj.to_dict())


@router.post("/template/create", summary="Créer un template")
async def create_template(template_in: TemplateCreate):
    """
    Créer un nouveau template.
    """
    # Check if name already exists
    existing = await template_controller.get_by_name(template_in.name)
    if existing:
        return Fail(code=400, msg="Un template avec ce nom existe déjà")
    
    new_template = await template_controller.create(obj_in=template_in)
    return Success(msg="Template créé avec succès", data={"id": new_template.id})


@router.post("/template/update", summary="Modifier un template")
async def update_template(template_in: TemplateUpdate):
    """
    Mettre à jour un template.
    """
    await template_controller.update(id=template_in.id, obj_in=template_in)
    return Success(msg="Template modifié avec succès")


@router.delete("/template/delete", summary="Supprimer un template")
async def delete_template(
    template_id: int = Query(..., description="ID du template"),
):
    """
    Supprimer un template.
    """
    await template_controller.remove(id=template_id)
    return Success(msg="Template supprimé avec succès")


# ==================== NOTIFICATIONS ====================

@router.get("/list", summary="Liste des notifications")
async def list_notifications(
    page: int = Query(1, description="Numéro de page"),
    page_size: int = Query(20, description="Éléments par page"),
    search: str = Query("", description="Recherche par email ou sujet"),
    status: str = Query(None, description="Filtrer par statut"),
    notification_type: str = Query(None, description="Filtrer par type"),
):
    """
    Récupérer la liste des notifications avec pagination.
    """
    q = Q()
    if search:
        q &= (
            Q(recipient_email__icontains=search) |
            Q(subject__icontains=search) |
            Q(recipient_name__icontains=search)
        )
    if status:
        q &= Q(status=status)
    if notification_type:
        q &= Q(notification_type=notification_type)
    
    total, notification_objs = await notification_controller.list(
        page=page,
        page_size=page_size,
        search=q,
        order=["-created_at"]
    )
    
    data = []
    for obj in notification_objs:
        d = await obj.to_dict()
        # Convert datetime to string
        for key in ['scheduled_at', 'sent_at', 'created_at', 'updated_at']:
            if d.get(key):
                d[key] = str(d[key])
        data.append(d)
    
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="Détail d'une notification")
async def get_notification(
    notification_id: int = Query(..., description="ID de la notification"),
):
    """
    Récupérer les détails d'une notification.
    """
    notification_obj = await notification_controller.get(id=notification_id)
    if not notification_obj:
        return Fail(code=404, msg="Notification non trouvée")
    
    d = await notification_obj.to_dict()
    for key in ['scheduled_at', 'sent_at', 'created_at', 'updated_at']:
        if d.get(key):
            d[key] = str(d[key])
    
    return Success(data=d)


@router.post("/create", summary="Créer une notification")
async def create_notification(notification_in: NotificationCreate):
    """
    Créer une nouvelle notification.
    """
    new_notification = await notification_controller.create_notification(obj_in=notification_in)
    return Success(msg="Notification créée avec succès", data={"id": new_notification.id})


@router.post("/send-bulk", summary="Envoi en masse")
async def send_bulk_notifications(bulk_in: BulkNotificationCreate):
    """
    Créer des notifications pour plusieurs étudiants.
    """
    notifications = await notification_controller.create_bulk_notifications(
        student_ids=bulk_in.recipient_ids,
        subject=bulk_in.subject,
        body=bulk_in.body,
        notification_type=bulk_in.notification_type
    )
    
    return Success(
        msg=f"{len(notifications)} notification(s) créée(s) avec succès",
        data={"count": len(notifications)}
    )


@router.post("/mark-sent", summary="Marquer comme envoyé")
async def mark_notification_sent(
    notification_id: int = Query(..., description="ID de la notification"),
):
    """
    Marquer une notification comme envoyée (simulation).
    """
    notification = await notification_controller.mark_as_sent(notification_id)
    if notification:
        return Success(msg="Notification marquée comme envoyée")
    return Fail(code=404, msg="Notification non trouvée")


@router.delete("/delete", summary="Supprimer une notification")
async def delete_notification(
    notification_id: int = Query(..., description="ID de la notification"),
):
    """
    Supprimer une notification.
    """
    await notification_controller.remove(id=notification_id)
    return Success(msg="Notification supprimée avec succès")


@router.get("/stats", summary="Statistiques")
async def get_stats():
    """
    Récupérer les statistiques des notifications.
    """
    stats = await notification_controller.get_stats()
    return Success(data=stats)


@router.get("/options", summary="Options pour les formulaires")
async def get_options():
    """
    Récupérer les options pour les selects.
    """
    return Success(data={
        "types": [
            {"value": "general", "label": "Général"},
            {"value": "reminder", "label": "Rappel"},
            {"value": "confirmation", "label": "Confirmation"},
            {"value": "invoice", "label": "Facture"},
            {"value": "welcome", "label": "Bienvenue"},
            {"value": "session", "label": "Session"},
        ],
        "statuses": [
            {"value": "pending", "label": "En attente"},
            {"value": "sent", "label": "Envoyé"},
            {"value": "failed", "label": "Échec"},
            {"value": "cancelled", "label": "Annulé"},
        ],
    })
