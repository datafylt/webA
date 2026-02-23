"""
Notification Model - Formation Électro
"""

from tortoise import fields

from .base import BaseModel, TimestampMixin


class NotificationTemplate(BaseModel, TimestampMixin):
    """
    Modèle Template de notification
    """

    name = fields.CharField(max_length=100, unique=True, description="Nom du template")
    subject = fields.CharField(max_length=255, description="Sujet de l'email")
    body = fields.TextField(description="Corps du message (HTML supporté)")

    # Type de notification
    notification_type = fields.CharField(
        max_length=50, default="general", description="Type: general, reminder, confirmation, invoice, welcome"
    )

    # Variables disponibles
    variables = fields.TextField(null=True, description="Variables disponibles: {student_name}, {session_date}, etc.")

    is_active = fields.BooleanField(default=True, description="Template actif")

    class Meta:
        table = "notification_template"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Notification(BaseModel, TimestampMixin):
    """
    Modèle Notification envoyée
    """

    # Destinataire
    recipient_email = fields.CharField(max_length=255, index=True, description="Email destinataire")
    recipient_name = fields.CharField(max_length=200, null=True, description="Nom destinataire")

    # Lien optionnel vers étudiant
    student = fields.ForeignKeyField(
        "models.Student", related_name="notifications", on_delete=fields.SET_NULL, null=True
    )

    # Contenu
    subject = fields.CharField(max_length=255, description="Sujet")
    body = fields.TextField(description="Corps du message")

    # Type et template
    notification_type = fields.CharField(max_length=50, default="general", description="Type de notification")
    template = fields.ForeignKeyField(
        "models.NotificationTemplate", related_name="notifications", on_delete=fields.SET_NULL, null=True
    )

    # Statut d'envoi
    status = fields.CharField(
        max_length=20, default="pending", index=True, description="Statut: pending, sent, failed, cancelled"
    )

    # Dates
    scheduled_at = fields.DatetimeField(null=True, description="Date d'envoi programmé")
    sent_at = fields.DatetimeField(null=True, description="Date d'envoi effectif")

    # Erreur éventuelle
    error_message = fields.TextField(null=True, description="Message d'erreur si échec")

    class Meta:
        table = "notification"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} -> {self.recipient_email}"
