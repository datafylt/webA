"""
Email API Endpoints - SMTP Integration
"""

import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field, EmailStr

from app.core.config import settings, SMTP_PROVIDERS
from app.services.email_service import email_service
from app.controllers.notification import notification_controller
from app.controllers.student import student_controller
from app.schemas.base import Fail, Success

logger = logging.getLogger(__name__)

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════

class SendEmailRequest(BaseModel):
    """Requête d'envoi d'email"""
    to_email: EmailStr = Field(..., description="Email destinataire")
    to_name: Optional[str] = Field(None, description="Nom destinataire")
    subject: str = Field(..., min_length=1, description="Sujet")
    body_html: str = Field(..., min_length=1, description="Corps HTML")
    body_text: Optional[str] = Field(None, description="Corps texte")
    
    
class SendBulkEmailRequest(BaseModel):
    """Requête d'envoi d'emails en masse"""
    template_id: Optional[int] = Field(None, description="ID du template à utiliser")
    subject: str = Field(..., min_length=1, description="Sujet")
    body_html: str = Field(..., min_length=1, description="Corps HTML")
    recipient_type: str = Field("selected", description="Type: all, active, selected, session")
    selected_ids: Optional[List[int]] = Field(None, description="IDs des étudiants sélectionnés")
    session_id: Optional[int] = Field(None, description="ID de session (si recipient_type=session)")
    variables: Optional[dict] = Field(None, description="Variables globales")


class SMTPConfigRequest(BaseModel):
    """Configuration SMTP"""
    provider: str = Field("custom", description="Provider: gmail, outlook, sendgrid, custom")
    host: Optional[str] = Field(None, description="Serveur SMTP")
    port: Optional[int] = Field(None, description="Port SMTP")
    user: str = Field(..., description="Utilisateur SMTP")
    password: str = Field(..., description="Mot de passe SMTP")
    from_email: EmailStr = Field(..., description="Email expéditeur")
    from_name: str = Field("Formation Électro", description="Nom expéditeur")
    use_tls: bool = Field(True, description="Utiliser TLS")
    use_ssl: bool = Field(False, description="Utiliser SSL")


# ═══════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

@router.post("/send", summary="Envoyer un email")
async def send_email(request: SendEmailRequest):
    """
    Envoyer un email unique.
    """
    # Vérifier si mode test
    if settings.EMAIL_TEST_MODE:
        logger.info(f"[TEST MODE] Email simulé vers {request.to_email}: {request.subject}")
        
        # Créer une notification en base
        await notification_controller.create_notification(
            recipient_email=request.to_email,
            recipient_name=request.to_name,
            subject=request.subject,
            body=request.body_html,
            notification_type="manual",
            status="sent",  # Simulé comme envoyé
            sent_at=datetime.now()
        )
        
        return Success(
            msg="Email envoyé (mode test)",
            data={
                "success": True,
                "test_mode": True,
                "recipient": request.to_email,
                "sent_at": datetime.now().isoformat()
            }
        )
    
    # Envoi réel
    result = email_service.send_email(
        to_email=request.to_email,
        to_name=request.to_name,
        subject=request.subject,
        body_html=request.body_html,
        body_text=request.body_text
    )
    
    # Enregistrer en base
    status = "sent" if result["success"] else "failed"
    await notification_controller.create_notification(
        recipient_email=request.to_email,
        recipient_name=request.to_name,
        subject=request.subject,
        body=request.body_html,
        notification_type="manual",
        status=status,
        sent_at=datetime.now() if result["success"] else None,
        error_message=result.get("error")
    )
    
    if result["success"]:
        return Success(msg="Email envoyé avec succès", data=result)
    else:
        return Fail(code=500, msg=result.get("error", "Erreur d'envoi"))


@router.post("/send-bulk", summary="Envoyer des emails en masse")
async def send_bulk_emails(request: SendBulkEmailRequest):
    """
    Envoyer des emails à plusieurs destinataires.
    Supporte les variables de personnalisation.
    """
    # Récupérer les destinataires
    recipients = []
    
    if request.recipient_type == "all":
        # Tous les étudiants
        students = await student_controller.get_all_students()
        recipients = [
            {
                "email": s.email,
                "name": f"{s.first_name} {s.last_name}",
                "first_name": s.first_name,
                "last_name": s.last_name,
                "student_id": s.id
            }
            for s in students if s.email
        ]
        
    elif request.recipient_type == "active":
        # Étudiants actifs uniquement
        students = await student_controller.get_active_students()
        recipients = [
            {
                "email": s.email,
                "name": f"{s.first_name} {s.last_name}",
                "first_name": s.first_name,
                "last_name": s.last_name,
                "student_id": s.id
            }
            for s in students if s.email
        ]
        
    elif request.recipient_type == "selected" and request.selected_ids:
        # Étudiants sélectionnés
        for student_id in request.selected_ids:
            student = await student_controller.get(id=student_id)
            if student and student.email:
                recipients.append({
                    "email": student.email,
                    "name": f"{student.first_name} {student.last_name}",
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "student_id": student.id
                })
                
    elif request.recipient_type == "session" and request.session_id:
        # Étudiants inscrits à une session
        from app.controllers.session import session_controller
        enrollments = await session_controller.get_session_enrollments(request.session_id)
        for enrollment in enrollments:
            student = await student_controller.get(id=enrollment.student_id)
            if student and student.email:
                recipients.append({
                    "email": student.email,
                    "name": f"{student.first_name} {student.last_name}",
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "student_id": student.id
                })
    
    if not recipients:
        return Fail(code=400, msg="Aucun destinataire trouvé")
    
    # Mode test
    if settings.EMAIL_TEST_MODE:
        logger.info(f"[TEST MODE] Emails simulés vers {len(recipients)} destinataires")
        
        # Créer les notifications en base
        for recipient in recipients:
            personalized_subject = request.subject
            personalized_body = request.body_html
            
            for key, value in recipient.items():
                personalized_subject = personalized_subject.replace(f"{{{key}}}", str(value or ''))
                personalized_body = personalized_body.replace(f"{{{key}}}", str(value or ''))
            
            await notification_controller.create_notification(
                recipient_email=recipient["email"],
                recipient_name=recipient.get("name"),
                subject=personalized_subject,
                body=personalized_body,
                notification_type="bulk",
                status="sent",
                sent_at=datetime.now(),
                student_id=recipient.get("student_id")
            )
        
        return Success(
            msg=f"Emails envoyés (mode test) à {len(recipients)} destinataires",
            data={
                "sent_count": len(recipients),
                "failed_count": 0,
                "total": len(recipients),
                "test_mode": True
            }
        )
    
    # Envoi réel
    result = email_service.send_bulk_emails(
        recipients=recipients,
        subject=request.subject,
        body_html=request.body_html,
        variables=request.variables
    )
    
    # Enregistrer les résultats en base
    for email_result in result["results"]:
        recipient = next((r for r in recipients if r["email"] == email_result["recipient"]), {})
        
        personalized_subject = request.subject
        personalized_body = request.body_html
        for key, value in recipient.items():
            personalized_subject = personalized_subject.replace(f"{{{key}}}", str(value or ''))
            personalized_body = personalized_body.replace(f"{{{key}}}", str(value or ''))
        
        await notification_controller.create_notification(
            recipient_email=email_result["recipient"],
            recipient_name=recipient.get("name"),
            subject=personalized_subject,
            body=personalized_body,
            notification_type="bulk",
            status="sent" if email_result["success"] else "failed",
            sent_at=datetime.now() if email_result["success"] else None,
            error_message=email_result.get("error"),
            student_id=recipient.get("student_id")
        )
    
    return Success(
        msg=f"{result['sent_count']}/{result['total']} emails envoyés",
        data=result
    )


@router.post("/test-connection", summary="Tester la connexion SMTP")
async def test_smtp_connection():
    """
    Tester la connexion au serveur SMTP.
    """
    result = email_service.test_connection()
    
    if result["success"]:
        return Success(msg="Connexion SMTP réussie", data=result)
    else:
        return Fail(code=500, msg=f"Échec de connexion: {result.get('error')}")


@router.post("/test-send", summary="Envoyer un email de test")
async def send_test_email(
    to_email: EmailStr = Query(..., description="Email de test")
):
    """
    Envoyer un email de test pour vérifier la configuration.
    """
    test_html = """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #f59e0b;">⚡ Formation Électro</h1>
        <p>Ceci est un <strong>email de test</strong> pour vérifier la configuration SMTP.</p>
        <p>Si vous recevez cet email, la configuration fonctionne correctement! ✅</p>
        <hr style="border: 1px solid #eee; margin: 20px 0;">
        <p style="color: #666; font-size: 12px;">
            Envoyé depuis Formation Électro - {datetime}
        </p>
    </div>
    """.replace("{datetime}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Forcer l'envoi réel même en mode test
    original_test_mode = settings.EMAIL_TEST_MODE
    try:
        # Temporairement désactiver le mode test
        settings.EMAIL_TEST_MODE = False
        
        result = email_service.send_email(
            to_email=to_email,
            subject="✅ Test SMTP - Formation Électro",
            body_html=test_html
        )
    finally:
        settings.EMAIL_TEST_MODE = original_test_mode
    
    if result["success"]:
        return Success(msg=f"Email de test envoyé à {to_email}", data=result)
    else:
        return Fail(code=500, msg=result.get("error", "Erreur d'envoi"))


@router.get("/config", summary="Configuration SMTP actuelle")
async def get_smtp_config():
    """
    Récupérer la configuration SMTP actuelle (sans le mot de passe).
    """
    return Success(data={
        "host": settings.SMTP_HOST,
        "port": settings.SMTP_PORT,
        "user": settings.SMTP_USER,
        "from_email": settings.SMTP_FROM_EMAIL,
        "from_name": settings.SMTP_FROM_NAME,
        "use_tls": settings.SMTP_USE_TLS,
        "use_ssl": settings.SMTP_USE_SSL,
        "test_mode": settings.EMAIL_TEST_MODE,
        "password_configured": bool(settings.SMTP_PASSWORD),
    })


@router.get("/providers", summary="Liste des providers SMTP")
async def get_smtp_providers():
    """
    Récupérer la liste des providers SMTP préconfigurés.
    """
    return Success(data=SMTP_PROVIDERS)


@router.get("/stats", summary="Statistiques d'envoi")
async def get_email_stats():
    """
    Récupérer les statistiques d'envoi d'emails.
    """
    stats = await notification_controller.get_stats()
    return Success(data=stats)
