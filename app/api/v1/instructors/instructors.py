"""
Instructor API Endpoints - CRUD Operations
"""

import logging
from decimal import Decimal

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.instructor import instructor_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.instructors import InstructorCreate, InstructorUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


def serialize_instructor(obj: dict) -> dict:
    """Convert Decimal types for JSON"""
    if obj.get('hourly_rate') is not None:
        obj['hourly_rate'] = float(obj['hourly_rate'])
    return obj


@router.get("/list", summary="Liste des formateurs")
async def list_instructors(
    page: int = Query(1, description="Numéro de page"),
    page_size: int = Query(20, description="Éléments par page"),
    search: str = Query("", description="Recherche par nom ou email"),
    status: str = Query(None, description="Filtrer par statut"),
    specialization: str = Query(None, description="Filtrer par spécialisation"),
    available: bool = Query(None, description="Filtrer par disponibilité"),
):
    """
    Récupérer la liste des formateurs avec pagination.
    """
    q = Q()
    if search:
        q &= (
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    if status:
        q &= Q(status=status)
    if specialization:
        q &= Q(specialization=specialization)
    if available is not None:
        q &= Q(is_available=available)
    
    total, instructor_objs = await instructor_controller.list(
        page=page,
        page_size=page_size,
        search=q,
        order=["last_name", "first_name"]
    )
    
    data = []
    for obj in instructor_objs:
        d = await obj.to_dict()
        d = serialize_instructor(d)
        d['full_name'] = obj.full_name
        data.append(d)
    
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/all", summary="Tous les formateurs actifs")
async def get_all_active():
    """
    Récupérer tous les formateurs actifs (pour les selects).
    """
    instructors = await instructor_controller.get_active_instructors()
    data = []
    for obj in instructors:
        d = await obj.to_dict()
        d = serialize_instructor(d)
        d['full_name'] = obj.full_name
        data.append(d)
    
    return Success(data=data)


@router.get("/available", summary="Formateurs disponibles")
async def get_available():
    """
    Récupérer les formateurs disponibles pour assignation.
    """
    instructors = await instructor_controller.get_available_instructors()
    data = [{"id": i.id, "name": i.full_name, "specialization": i.specialization} for i in instructors]
    return Success(data=data)


@router.get("/get", summary="Détail d'un formateur")
async def get_instructor(
    instructor_id: int = Query(..., description="ID du formateur"),
):
    """
    Récupérer les détails d'un formateur.
    """
    instructor_obj = await instructor_controller.get(id=instructor_id)
    if not instructor_obj:
        return Fail(code=404, msg="Formateur non trouvé")
    
    d = await instructor_obj.to_dict()
    d = serialize_instructor(d)
    d['full_name'] = instructor_obj.full_name
    
    return Success(data=d)


@router.post("/create", summary="Créer un formateur")
async def create_instructor(instructor_in: InstructorCreate):
    """
    Créer un nouveau formateur.
    """
    # Check if email already exists
    if await instructor_controller.check_email_exists(instructor_in.email):
        return Fail(code=400, msg="Un formateur avec cet email existe déjà")
    
    new_instructor = await instructor_controller.create(obj_in=instructor_in)
    return Success(msg="Formateur créé avec succès", data={"id": new_instructor.id})


@router.post("/update", summary="Modifier un formateur")
async def update_instructor(instructor_in: InstructorUpdate):
    """
    Mettre à jour un formateur.
    """
    # Check if email is taken by another instructor
    if instructor_in.email:
        if await instructor_controller.check_email_exists(instructor_in.email, exclude_id=instructor_in.id):
            return Fail(code=400, msg="Un autre formateur utilise déjà cet email")
    
    await instructor_controller.update(id=instructor_in.id, obj_in=instructor_in)
    return Success(msg="Formateur modifié avec succès")


@router.delete("/delete", summary="Supprimer un formateur")
async def delete_instructor(
    instructor_id: int = Query(..., description="ID du formateur"),
):
    """
    Supprimer un formateur.
    """
    await instructor_controller.remove(id=instructor_id)
    return Success(msg="Formateur supprimé avec succès")


@router.get("/options", summary="Options pour les formulaires")
async def get_options():
    """
    Récupérer les options pour les selects.
    """
    return Success(data={
        "statuses": [
            {"value": "active", "label": "Actif"},
            {"value": "inactive", "label": "Inactif"},
            {"value": "on_leave", "label": "En congé"},
        ],
        "specializations": [
            {"value": "licence_c", "label": "Licence C - Compagnon"},
            {"value": "rca", "label": "RCA - Connexions Restreintes"},
            {"value": "rbq", "label": "RBQ - Constructeur Propriétaire"},
            {"value": "cmeq", "label": "CMEQ - Entrepreneur"},
            {"value": "sceau_rouge", "label": "Sceau Rouge"},
            {"value": "code", "label": "Code de construction"},
            {"value": "securite", "label": "Sécurité électrique"},
            {"value": "general", "label": "Formation générale"},
        ],
    })
