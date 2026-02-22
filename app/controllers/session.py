"""
Session Controller - Business logic for Session CRUD
"""

from datetime import date
from typing import Optional


from app.core.crud import CRUDBase
from app.models.session import Session, SessionEnrollment
from app.schemas.sessions import SessionCreate, SessionUpdate, EnrollmentCreate, EnrollmentUpdate


class SessionController(CRUDBase[Session, SessionCreate, SessionUpdate]):
    def __init__(self):
        super().__init__(model=Session)

    async def get_with_program(self, id: int) -> Optional[Session]:
        """Get session with program data"""
        return await self.model.filter(id=id).prefetch_related("program").first()

    async def get_upcoming_sessions(self, limit: int = 10):
        """Get upcoming sessions"""
        return await self.model.filter(
            start_date__gte=date.today(),
            status="scheduled"
        ).prefetch_related("program").order_by("start_date").limit(limit)

    async def get_sessions_by_program(self, program_id: int):
        """Get all sessions for a program"""
        return await self.model.filter(program_id=program_id).order_by("-start_date")

    async def get_enrollment_count(self, session_id: int) -> int:
        """Get number of enrolled students"""
        return await SessionEnrollment.filter(
            session_id=session_id,
            status__in=["enrolled", "completed"]
        ).count()

    async def get_available_spots(self, session_id: int) -> int:
        """Get available spots in session"""
        session = await self.get(id=session_id)
        enrolled = await self.get_enrollment_count(session_id)
        return max(0, session.max_participants - enrolled)


class EnrollmentController(CRUDBase[SessionEnrollment, EnrollmentCreate, EnrollmentUpdate]):
    def __init__(self):
        super().__init__(model=SessionEnrollment)

    async def get_by_session_student(self, session_id: int, student_id: int) -> Optional[SessionEnrollment]:
        """Check if student is enrolled in session"""
        return await self.model.filter(session_id=session_id, student_id=student_id).first()

    async def is_enrolled(self, session_id: int, student_id: int) -> bool:
        """Check if student is enrolled"""
        return await self.model.filter(session_id=session_id, student_id=student_id).exists()

    async def get_session_enrollments(self, session_id: int):
        """Get all enrollments for a session"""
        return await self.model.filter(session_id=session_id).prefetch_related("student")

    async def get_student_enrollments(self, student_id: int):
        """Get all enrollments for a student"""
        return await self.model.filter(student_id=student_id).prefetch_related("session", "session__program")


session_controller = SessionController()
enrollment_controller = EnrollmentController()
