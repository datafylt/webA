"""
Session API Endpoints - CRUD Operations
"""

import logging
from datetime import date, time
from decimal import Decimal

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.session import session_controller, enrollment_controller
from app.models.session import Session, SessionEnrollment
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.sessions import SessionCreate, SessionUpdate, EnrollmentCreate, EnrollmentUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


def serialize_session(obj: dict) -> dict:
    """Convert non-JSON-serializable types"""
    if obj.get('price') is not None:
        obj['price'] = float(obj['price'])
    if obj.get('start_date'):
        obj['start_date'] = str(obj['start_date'])
    if obj.get('end_date'):
        obj['end_date'] = str(obj['end_date'])
    if obj.get('start_time'):
        obj['start_time'] = str(obj['start_time'])
    if obj.get('end_time'):
        obj['end_time'] = str(obj['end_time'])
    return obj


@router.get("/list", summary="Liste des sessions")
async def list_sessions(
    page: int = Query(1, description="Numéro de page"),
    page_size: int = Query(20, description="Éléments par page"),
    search: str = Query("", description="Recherche par titre"),
    program_id: int = Query(None, description="Filtrer par programme"),
    status: str = Query(None, description="Filtrer par statut"),
    upcoming: bool = Query(False, description="Sessions à venir seulement"),
):
    """
    Récupérer la liste des sessions avec pagination.
    """
    q = Q()
    if search:
        q &= Q(title__icontains=search)
    if program_id:
        q &= Q(program_id=program_id)
    if status:
        q &= Q(status=status)
    if upcoming:
        q &= Q(start_date__gte=date.today())
    
    total, session_objs = await session_controller.list(
        page=page, 
        page_size=page_size, 
        search=q,
        order=["-start_date"]
    )
    
    data = []
    for obj in session_objs:
        await obj.fetch_related("program")
        d = await obj.to_dict()
        d = serialize_session(d)
        # Add program info
        if obj.program:
            d['program_name'] = obj.program.name
            d['program_code'] = obj.program.code
        # Add enrollment count
        d['enrolled_count'] = await session_controller.get_enrollment_count(obj.id)
        d['available_spots'] = obj.max_participants - d['enrolled_count']
        data.append(d)
    
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="Détail d'une session")
async def get_session(
    session_id: int = Query(..., description="ID de la session"),
):
    """
    Récupérer les détails d'une session.
    """
    session_obj = await session_controller.get_with_program(session_id)
    if not session_obj:
        return Fail(code=404, msg="Session non trouvée")
    
    d = await session_obj.to_dict()
    d = serialize_session(d)
    
    if session_obj.program:
        d['program_name'] = session_obj.program.name
        d['program_code'] = session_obj.program.code
    
    d['enrolled_count'] = await session_controller.get_enrollment_count(session_obj.id)
    d['available_spots'] = session_obj.max_participants - d['enrolled_count']
    
    return Success(data=d)


@router.post("/create", summary="Créer une session")
async def create_session(session_in: SessionCreate):
    """
    Créer une nouvelle session.
    """
    new_session = await session_controller.create(obj_in=session_in)
    return Success(msg="Session créée avec succès", data={"id": new_session.id})


@router.post("/update", summary="Modifier une session")
async def update_session(session_in: SessionUpdate):
    """
    Mettre à jour une session existante.
    """
    await session_controller.update(id=session_in.id, obj_in=session_in)
    return Success(msg="Session modifiée avec succès")


@router.delete("/delete", summary="Supprimer une session")
async def delete_session(
    session_id: int = Query(..., description="ID de la session"),
):
    """
    Supprimer une session.
    """
    # Check for enrollments
    enrollment_count = await session_controller.get_enrollment_count(session_id)
    if enrollment_count > 0:
        return Fail(code=400, msg=f"Impossible de supprimer: {enrollment_count} inscriptions actives")
    
    await session_controller.remove(id=session_id)
    return Success(msg="Session supprimée avec succès")


@router.get("/upcoming", summary="Sessions à venir")
async def get_upcoming_sessions(
    limit: int = Query(10, description="Nombre de sessions"),
):
    """
    Récupérer les prochaines sessions.
    """
    sessions = await session_controller.get_upcoming_sessions(limit=limit)
    data = []
    for obj in sessions:
        d = await obj.to_dict()
        d = serialize_session(d)
        if obj.program:
            d['program_name'] = obj.program.name
        d['enrolled_count'] = await session_controller.get_enrollment_count(obj.id)
        data.append(d)
    
    return Success(data=data)


@router.get("/options", summary="Options pour les formulaires")
async def get_options():
    """
    Récupérer les options pour les selects.
    """
    return Success(data={
        "location_types": [
            {"value": "in_person", "label": "En personne"},
            {"value": "online", "label": "En ligne"},
            {"value": "hybrid", "label": "Hybride"},
        ],
        "statuses": [
            {"value": "scheduled", "label": "Planifiée"},
            {"value": "in_progress", "label": "En cours"},
            {"value": "completed", "label": "Terminée"},
            {"value": "cancelled", "label": "Annulée"},
        ],
    })


# ==================== ENROLLMENTS ====================

@router.get("/enrollments", summary="Inscriptions d'une session")
async def get_session_enrollments(
    session_id: int = Query(..., description="ID de la session"),
):
    """
    Récupérer toutes les inscriptions d'une session.
    """
    enrollments = await enrollment_controller.get_session_enrollments(session_id)
    data = []
    for e in enrollments:
        d = await e.to_dict()
        if d.get('amount_paid') is not None:
            d['amount_paid'] = float(d['amount_paid'])
        if d.get('enrolled_at'):
            d['enrolled_at'] = str(d['enrolled_at'])
        # Add student info
        if e.student:
            d['student_name'] = f"{e.student.first_name} {e.student.last_name}"
            d['student_email'] = e.student.email
        data.append(d)
    
    return Success(data=data)


@router.post("/enroll", summary="Inscrire un étudiant")
async def enroll_student(enrollment_in: EnrollmentCreate):
    """
    Inscrire un étudiant à une session.
    """
    # Check if already enrolled
    if await enrollment_controller.is_enrolled(enrollment_in.session_id, enrollment_in.student_id):
        return Fail(code=400, msg="L'étudiant est déjà inscrit à cette session")
    
    # Check available spots
    available = await session_controller.get_available_spots(enrollment_in.session_id)
    if available <= 0:
        return Fail(code=400, msg="Aucune place disponible")
    
    new_enrollment = await enrollment_controller.create(obj_in=enrollment_in)
    return Success(msg="Inscription réussie", data={"id": new_enrollment.id})


@router.post("/enrollment/update", summary="Modifier une inscription")
async def update_enrollment(enrollment_in: EnrollmentUpdate):
    """
    Modifier une inscription existante.
    """
    await enrollment_controller.update(id=enrollment_in.id, obj_in=enrollment_in)
    return Success(msg="Inscription modifiée avec succès")


@router.delete("/enrollment/delete", summary="Supprimer une inscription")
async def delete_enrollment(
    enrollment_id: int = Query(..., description="ID de l'inscription"),
):
    """
    Supprimer une inscription.
    """
    await enrollment_controller.remove(id=enrollment_id)
    return Success(msg="Inscription supprimée avec succès")
