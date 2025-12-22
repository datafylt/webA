"""
Notification Controller - Business logic for Notification CRUD
"""

from datetime import datetime
from typing import Optional, List

from app.core.crud import CRUDBase
from app.models.notification import Notification, NotificationTemplate
from app.models.student import Student
from app.schemas.notifications import NotificationCreate, TemplateCreate, TemplateUpdate


class TemplateController(CRUDBase[NotificationTemplate, TemplateCreate, TemplateUpdate]):
    def __init__(self):
        super().__init__(model=NotificationTemplate)

    async def get_by_name(self, name: str) -> Optional[NotificationTemplate]:
        """Get template by name"""
        return await self.model.filter(name=name).first()

    async def get_active_templates(self):
        """Get all active templates"""
        return await self.model.filter(is_active=True).order_by("name")

    async def get_by_type(self, notification_type: str):
        """Get templates by type"""
        return await self.model.filter(
            notification_type=notification_type,
            is_active=True
        ).order_by("name")


class NotificationController(CRUDBase[Notification, NotificationCreate, NotificationCreate]):
    def __init__(self):
        super().__init__(model=Notification)

    async def create_notification(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        recipient_name: Optional[str] = None,
        student_id: Optional[int] = None,
        notification_type: str = "general",
        template_id: Optional[int] = None,
        scheduled_at: Optional[datetime] = None,
        status: str = "pending",
        sent_at: Optional[datetime] = None,
        error_message: Optional[str] = None,
    ) -> Notification:
        """Create a new notification with flexible parameters"""
        notification = await self.model.create(
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            student_id=student_id,
            subject=subject,
            body=body,
            notification_type=notification_type,
            template_id=template_id,
            scheduled_at=scheduled_at,
            status=status,
            sent_at=sent_at,
            error_message=error_message,
        )
        return notification

    async def create_bulk_notifications(self, student_ids: List[int], subject: str, body: str, notification_type: str = "general") -> List[Notification]:
        """Create notifications for multiple students"""
        notifications = []
        students = await Student.filter(id__in=student_ids)
        
        for student in students:
            # Replace variables in body
            personalized_body = body.replace("{student_name}", student.full_name)
            personalized_body = personalized_body.replace("{first_name}", student.first_name)
            personalized_body = personalized_body.replace("{last_name}", student.last_name)
            personalized_body = personalized_body.replace("{email}", student.email)
            
            notification = await self.model.create(
                recipient_email=student.email,
                recipient_name=student.full_name,
                student_id=student.id,
                subject=subject,
                body=personalized_body,
                notification_type=notification_type,
                status="pending"
            )
            notifications.append(notification)
        
        return notifications

    async def mark_as_sent(self, notification_id: int) -> Optional[Notification]:
        """Mark notification as sent"""
        notification = await self.get(id=notification_id)
        if notification:
            notification.status = "sent"
            notification.sent_at = datetime.now()
            await notification.save()
        return notification

    async def mark_as_failed(self, notification_id: int, error_message: str) -> Optional[Notification]:
        """Mark notification as failed"""
        notification = await self.get(id=notification_id)
        if notification:
            notification.status = "failed"
            notification.error_message = error_message
            await notification.save()
        return notification

    async def get_pending_notifications(self):
        """Get all pending notifications"""
        return await self.model.filter(status="pending").order_by("created_at")

    async def get_student_notifications(self, student_id: int):
        """Get all notifications for a student"""
        return await self.model.filter(student_id=student_id).order_by("-created_at")

    async def get_stats(self):
        """Get notification statistics"""
        from datetime import timedelta
        
        total = await self.model.all().count()
        sent = await self.model.filter(status="sent").count()
        pending = await self.model.filter(status="pending").count()
        failed = await self.model.filter(status="failed").count()
        
        # Dernières 24h
        yesterday = datetime.now() - timedelta(days=1)
        sent_24h = await self.model.filter(
            status="sent",
            sent_at__gte=yesterday
        ).count()
        
        return {
            "total": total,
            "sent": sent,
            "pending": pending,
            "failed": failed,
            "sent_24h": sent_24h,
            "success_rate": round(sent / total * 100, 1) if total > 0 else 0,
        }


template_controller = TemplateController()
notification_controller = NotificationController()
