"""
Instructor Controller - Business logic for Instructor CRUD
"""

from typing import Optional

from app.core.crud import CRUDBase
from app.models.instructor import Instructor
from app.schemas.instructors import InstructorCreate, InstructorUpdate


class InstructorController(CRUDBase[Instructor, InstructorCreate, InstructorUpdate]):
    def __init__(self):
        super().__init__(model=Instructor)

    async def get_by_email(self, email: str) -> Optional[Instructor]:
        """Get instructor by email"""
        return await self.model.filter(email=email).first()

    async def check_email_exists(self, email: str, exclude_id: int = None) -> bool:
        """Check if email is already used by another instructor"""
        query = self.model.filter(email=email)
        if exclude_id:
            query = query.exclude(id=exclude_id)
        return await query.exists()

    async def get_active_instructors(self):
        """Get all active instructors"""
        return await self.model.filter(status="active", is_available=True).order_by("last_name")

    async def get_available_instructors(self):
        """Get available instructors for assignment"""
        return await self.model.filter(
            status="active",
            is_available=True
        ).order_by("last_name", "first_name")

    async def update_status(self, id: int, status: str) -> Optional[Instructor]:
        """Update instructor status"""
        instructor = await self.get(id=id)
        if instructor:
            instructor.status = status
            await instructor.save()
        return instructor

    async def get_by_specialization(self, specialization: str):
        """Get instructors by specialization"""
        return await self.model.filter(
            specialization=specialization,
            status="active"
        ).order_by("last_name")


instructor_controller = InstructorController()
