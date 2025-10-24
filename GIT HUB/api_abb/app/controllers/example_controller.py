from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.schemas import ExampleCreate, ExampleUpdate, ExampleResponse
from app.services.example_service import example_service


# Router para agrupar endpoints relacionados
router = APIRouter()


@router.post("/examples", response_model=ExampleResponse, status_code=status.HTTP_201_CREATED)
async def create_example(example: ExampleCreate):
    """
    Crea un nuevo ejemplo.
    
    Args:
        example: Datos del ejemplo a crear
        
    Returns:
        El ejemplo creado con su ID asignado
    """
    return example_service.create(example)


@router.get("/examples", response_model=List[ExampleResponse])
async def get_all_examples():
    """
    Obtiene todos los ejemplos.
    
    Returns:
        Lista de todos los ejemplos
    """
    return example_service.get_all()


@router.get("/examples/{example_id}", response_model=ExampleResponse)
async def get_example(example_id: int):
    """
    Obtiene un ejemplo específico por su ID.
    
    Args:
        example_id: ID del ejemplo a buscar
        
    Returns:
        El ejemplo encontrado
        
    Raises:
        HTTPException: Si el ejemplo no existe
    """
    example = example_service.get_by_id(example_id)
    if not example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ejemplo con ID {example_id} no encontrado"
        )
    return example


@router.put("/examples/{example_id}", response_model=ExampleResponse)
async def update_example(example_id: int, example: ExampleUpdate):
    """
    Actualiza un ejemplo existente.
    
    Args:
        example_id: ID del ejemplo a actualizar
        example: Datos a actualizar
        
    Returns:
        El ejemplo actualizado
        
    Raises:
        HTTPException: Si el ejemplo no existe
    """
    updated_example = example_service.update(example_id, example)
    if not updated_example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ejemplo con ID {example_id} no encontrado"
        )
    return updated_example


@router.delete("/examples/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example(example_id: int):
    """
    Elimina un ejemplo.
    
    Args:
        example_id: ID del ejemplo a eliminar
        
    Raises:
        HTTPException: Si el ejemplo no existe
    """
    deleted = example_service.delete(example_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ejemplo con ID {example_id} no encontrado"
        )
