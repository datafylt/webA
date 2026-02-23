"""
Student API Endpoints - CRUD Operations
"""

import logging

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.student import student_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.students import StudentCreate, StudentUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="Liste des étudiants")
async def list_students(
    page: int = Query(1, description="Numéro de page"),
    page_size: int = Query(10, description="Éléments par page"),
    search: str = Query("", description="Recherche (nom, email, téléphone)"),
    status: str = Query("", description="Filtrer par statut"),
    goal: str = Query("", description="Filtrer par programme"),
):
    """
    Récupérer la liste des étudiants avec pagination et filtres.
    """
    q = Q()
    if search:
        q &= (
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
        )
    if status:
        q &= Q(status=status)
    if goal:
        q &= Q(goal=goal)

    total, student_objs = await student_controller.list(page=page, page_size=page_size, search=q, order=["-created_at"])
    data = [await obj.to_dict() for obj in student_objs]

    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="Détail d'un étudiant")
async def get_student(
    student_id: int = Query(..., description="ID de l'étudiant"),
):
    """
    Récupérer les détails d'un étudiant par son ID.
    """
    student_obj = await student_controller.get(id=student_id)
    student_dict = await student_obj.to_dict()
    return Success(data=student_dict)


@router.post("/create", summary="Créer un étudiant")
async def create_student(student_in: StudentCreate):
    """
    Créer un nouvel étudiant.
    """
    # Vérifier si l'email existe déjà
    if await student_controller.check_email_exists(student_in.email):
        return Fail(code=400, msg="Un étudiant avec cet email existe déjà")

    new_student = await student_controller.create(obj_in=student_in)
    return Success(msg="Étudiant créé avec succès", data={"id": new_student.id})


@router.post("/update", summary="Modifier un étudiant")
async def update_student(student_in: StudentUpdate):
    """
    Mettre à jour un étudiant existant.
    """
    # Vérifier si l'email existe déjà (si changé)
    if student_in.email:
        if await student_controller.check_email_exists(student_in.email, exclude_id=student_in.id):
            return Fail(code=400, msg="Un étudiant avec cet email existe déjà")

    await student_controller.update(id=student_in.id, obj_in=student_in)
    return Success(msg="Étudiant modifié avec succès")


@router.delete("/delete", summary="Supprimer un étudiant")
async def delete_student(
    student_id: int = Query(..., description="ID de l'étudiant"),
):
    """
    Supprimer un étudiant.
    """
    await student_controller.remove(id=student_id)
    return Success(msg="Étudiant supprimé avec succès")


@router.post("/bulk-delete", summary="Supprimer plusieurs étudiants")
async def bulk_delete_students(ids: list[int]):
    """
    Supprimer plusieurs étudiants à la fois.
    """
    deleted_count = await student_controller.bulk_delete(ids)
    return Success(msg=f"{deleted_count} étudiant(s) supprimé(s)")


@router.post("/bulk-status", summary="Changer le statut de plusieurs étudiants")
async def bulk_update_status(
    ids: list[int],
    status: str = Query(..., description="Nouveau statut: active, inactive, expired"),
):
    """
    Changer le statut de plusieurs étudiants.
    """
    if status not in ["active", "inactive", "expired"]:
        return Fail(code=400, msg="Statut invalide")

    updated_count = await student_controller.bulk_update_status(ids, status)
    return Success(msg=f"{updated_count} étudiant(s) mis à jour")


@router.get("/options", summary="Options pour les formulaires")
async def get_options():
    """
    Récupérer les options pour les selects (goal, status).
    """
    return Success(
        data={
            "goals": [
                {"value": "licence_c", "label": "Licence C - Compagnon Électricien"},
                {"value": "rca", "label": "RCA - Connexions Restreintes"},
                {"value": "rbq", "label": "RBQ - Constructeur Propriétaire"},
                {"value": "cmeq", "label": "CMEQ - Entrepreneur Électricien"},
                {"value": "sceau_rouge", "label": "Sceau Rouge - Interprovincial"},
                {"value": "custom", "label": "Formation sur mesure"},
            ],
            "statuses": [
                {"value": "active", "label": "Actif"},
                {"value": "inactive", "label": "Inactif"},
                {"value": "expired", "label": "Expiré"},
            ],
        }
    )
