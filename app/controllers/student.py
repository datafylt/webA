"""
Student Controller - Business logic for Student CRUD
"""

from typing import Optional

from app.core.crud import CRUDBase
from app.models.student import Student
from app.schemas.students import StudentCreate, StudentUpdate


class StudentController(CRUDBase[Student, StudentCreate, StudentUpdate]):
    def __init__(self):
        super().__init__(model=Student)

    async def get_by_email(self, email: str) -> Optional[Student]:
        """Get student by email"""
        return await self.model.filter(email=email).first()

    async def check_email_exists(self, email: str, exclude_id: int = None) -> bool:
        """Check if email already exists (optionally excluding a specific ID)"""
        query = self.model.filter(email=email)
        if exclude_id:
            query = query.exclude(id=exclude_id)
        return await query.exists()

    async def update_status(self, id: int, status: str) -> Student:
        """Update student status"""
        student = await self.get(id=id)
        student.status = status
        await student.save()
        return student

    async def bulk_update_status(self, ids: list[int], status: str) -> int:
        """Bulk update status for multiple students"""
        return await self.model.filter(id__in=ids).update(status=status)

    async def bulk_delete(self, ids: list[int]) -> int:
        """Bulk delete multiple students"""
        return await self.model.filter(id__in=ids).delete()

    async def get_all_students(self):
        """Get all students"""
        return await self.model.all().order_by("last_name", "first_name")

    async def get_active_students(self):
        """Get active students only"""
        return await self.model.filter(status="active").order_by("last_name", "first_name")


student_controller = StudentController()
