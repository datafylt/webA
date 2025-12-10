"""
Program API Endpoints - CRUD Operations
"""

import logging

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.program import program_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.programs import ProgramCreate, ProgramUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="Liste des programmes")
async def list_programs(
    page: int = Query(1, description="Numéro de page"),
    page_size: int = Query(20, description="Éléments par page"),
    search: str = Query("", description="Recherche par nom"),
    is_active: bool = Query(None, description="Filtrer par statut actif"),
):
    """
    Récupérer la liste des programmes avec pagination.
    """
    q = Q()
    if search:
        q &= Q(name__icontains=search) | Q(code__icontains=search)
    if is_active is not None:
        q &= Q(is_active=is_active)
    
    total, program_objs = await program_controller.list(
        page=page, 
        page_size=page_size, 
        search=q,
        order=["display_order", "name"]
    )
    data = []
    for obj in program_objs:
        d = await obj.to_dict()
        # Convert Decimal to float for JSON serialization
        if 'price' in d and d['price'] is not None:
            d['price'] = float(d['price'])
        data.append(d)
    
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/all", summary="Tous les programmes actifs")
async def get_all_active_programs():
    """
    Récupérer tous les programmes actifs (pour les selects).
    """
    programs = await program_controller.get_active_programs()
    data = []
    for obj in programs:
        d = await obj.to_dict()
        if 'price' in d and d['price'] is not None:
            d['price'] = float(d['price'])
        data.append(d)
    return Success(data=data)


@router.get("/get", summary="Détail d'un programme")
async def get_program(
    program_id: int = Query(..., description="ID du programme"),
):
    """
    Récupérer les détails d'un programme par son ID.
    """
    program_obj = await program_controller.get(id=program_id)
    program_dict = await program_obj.to_dict()
    # Convert Decimal to float
    if 'price' in program_dict and program_dict['price'] is not None:
        program_dict['price'] = float(program_dict['price'])
    return Success(data=program_dict)


@router.post("/create", summary="Créer un programme")
async def create_program(program_in: ProgramCreate):
    """
    Créer un nouveau programme.
    """
    # Vérifier si le code existe déjà
    if await program_controller.check_code_exists(program_in.code):
        return Fail(code=400, msg="Un programme avec ce code existe déjà")
    
    new_program = await program_controller.create(obj_in=program_in)
    return Success(msg="Programme créé avec succès", data={"id": new_program.id})


@router.post("/update", summary="Modifier un programme")
async def update_program(program_in: ProgramUpdate):
    """
    Mettre à jour un programme existant.
    """
    # Vérifier si le code existe déjà (si changé)
    if program_in.code:
        if await program_controller.check_code_exists(program_in.code, exclude_id=program_in.id):
            return Fail(code=400, msg="Un programme avec ce code existe déjà")
    
    await program_controller.update(id=program_in.id, obj_in=program_in)
    return Success(msg="Programme modifié avec succès")


@router.delete("/delete", summary="Supprimer un programme")
async def delete_program(
    program_id: int = Query(..., description="ID du programme"),
):
    """
    Supprimer un programme.
    """
    await program_controller.remove(id=program_id)
    return Success(msg="Programme supprimé avec succès")


@router.get("/options", summary="Options pour les formulaires")
async def get_options():
    """
    Récupérer les options pour les selects.
    """
    return Success(data={
        "exam_types": [
            {"value": "emploi_quebec", "label": "Emploi-Québec"},
            {"value": "cmeq", "label": "CMEQ"},
            {"value": "rbq", "label": "RBQ"},
            {"value": "sceau_rouge", "label": "Sceau Rouge (Interprovincial)"},
        ],
        "colors": [
            {"value": "#0277BC", "label": "Bleu"},
            {"value": "#4CAF50", "label": "Vert"},
            {"value": "#FF9800", "label": "Orange"},
            {"value": "#9C27B0", "label": "Violet"},
            {"value": "#F44336", "label": "Rouge"},
            {"value": "#607D8B", "label": "Gris"},
        ],
        "icons": [
            {"value": "mdi:lightning-bolt", "label": "Éclair"},
            {"value": "mdi:tools", "label": "Outils"},
            {"value": "mdi:home-city", "label": "Bâtiment"},
            {"value": "mdi:office-building-marker", "label": "Bureau"},
            {"value": "mdi:certificate", "label": "Certificat"},
            {"value": "mdi:school", "label": "École"},
        ],
    })
