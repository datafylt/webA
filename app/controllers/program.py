"""
Program Controller - Business logic for Program CRUD
"""

from typing import Optional

from app.core.crud import CRUDBase
from app.models.program import Program
from app.schemas.programs import ProgramCreate, ProgramUpdate


class ProgramController(CRUDBase[Program, ProgramCreate, ProgramUpdate]):
    def __init__(self):
        super().__init__(model=Program)

    async def get_by_code(self, code: str) -> Optional[Program]:
        """Get program by code"""
        return await self.model.filter(code=code).first()

    async def check_code_exists(self, code: str, exclude_id: int = None) -> bool:
        """Check if code already exists"""
        query = self.model.filter(code=code)
        if exclude_id:
            query = query.exclude(id=exclude_id)
        return await query.exists()

    async def get_active_programs(self):
        """Get all active programs"""
        return await self.model.filter(is_active=True).order_by("display_order", "name")

    async def update_display_order(self, id: int, order: int) -> Program:
        """Update program display order"""
        program = await self.get(id=id)
        program.display_order = order
        await program.save()
        return program


program_controller = ProgramController()
