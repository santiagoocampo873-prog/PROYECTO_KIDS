from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.schemas import (
    ChildCreate,
    ChildResponse,
    TreeResponse,
    TraversalResponse,
    MessageResponse
)
from app.services.abb_service import abb_service


# Router para agrupar todos los endpoints relacionados con el ABB
# Se usará el prefijo "/abb" en el archivo main.py
router = APIRouter()


# ==================== ENDPOINTS PARA AGREGAR NIÑOS ====================

@router.post("/children", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_child(child: ChildCreate):
    """
    Agrega un nuevo niño al Árbol Binario de Búsqueda.
    
    El ID del niño se usa como clave para ubicar el nodo en el árbol:
    - Si el ID es menor que el nodo actual, se coloca a la izquierda
    - Si el ID es mayor que el nodo actual, se coloca a la derecha
    - Si el ID ya existe, se rechaza la inserción
    
    Args:
        child: Datos del niño a agregar (ID, nombre, edad)
        
    Returns:
        Diccionario con el resultado de la operación y los datos del niño agregado
        
    Raises:
        HTTPException 409: Si el ID del niño ya existe en el árbol
    """
    # Llamar al servicio para agregar el niño
    result = abb_service.add_child(child)
    
    # Si la inserción falló porque el ID ya existe
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=result["message"]
        )
    
    # Retornar el resultado exitoso
    return result


# ==================== ENDPOINTS PARA BUSCAR NIÑOS ====================

@router.get("/children/{child_id}", response_model=ChildResponse)
async def get_child_by_id(child_id: int):
    """
    Busca un niño en el árbol por su ID.
    
    La búsqueda en un ABB es eficiente porque descarta la mitad de los nodos
    en cada comparación:
    - Si el ID buscado es igual al nodo actual, se encontró
    - Si es menor, se busca en el subárbol izquierdo
    - Si es mayor, se busca en el subárbol derecho
    
    Args:
        child_id: ID del niño a buscar
        
    Returns:
        Datos del niño encontrado (ID, nombre, edad)
        
    Raises:
        HTTPException 404: Si el niño no existe en el árbol
    """
    # Buscar el niño en el árbol
    child = abb_service.search_child(child_id)
    
    # Si no se encontró, lanzar excepción 404
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Niño con ID {child_id} no encontrado en el árbol"
        )
    
    # Retornar los datos del niño encontrado
    return child


@router.get("/children", response_model=List[ChildResponse])
async def get_all_children():
    """
    Obtiene todos los niños del árbol ordenados por ID (de menor a mayor).
    
    Utiliza el recorrido inorden del ABB, que garantiza que los nodos
    se visiten en orden ascendente.
    
    Returns:
        Lista de niños ordenada por ID
    """
    # Obtener todos los niños ordenados
    return abb_service.get_all_children()


# ==================== ENDPOINTS PARA VISUALIZAR EL ÁRBOL ====================

@router.get("/tree", response_model=TreeResponse)
async def get_tree_structure():
    """
    Obtiene la estructura completa del árbol en formato jerárquico.
    
    Muestra cada nodo con sus hijos izquierdo y derecho, permitiendo
    visualizar la organización del ABB.
    
    Returns:
        Estructura del árbol con la raíz y todos sus descendientes
    """
    # Obtener la estructura del árbol
    return abb_service.get_tree_structure()


# ==================== ENDPOINTS PARA RECORRIDOS DEL ÁRBOL ====================

@router.get("/traversal/inorder", response_model=TraversalResponse)
async def get_inorder_traversal():
    """
    Obtiene el recorrido inorden del árbol (izquierda - raíz - derecha).
    
    Este recorrido visita los nodos en orden ascendente por ID.
    Es útil para obtener los datos ordenados del menor al mayor.
    
    Orden de visita:
    1. Subárbol izquierdo
    2. Nodo raíz
    3. Subárbol derecho
    
    Returns:
        Lista de niños en orden inorden
    """
    # Obtener recorrido inorden
    return abb_service.get_inorder_traversal()


@router.get("/traversal/preorder", response_model=TraversalResponse)
async def get_preorder_traversal():
    """
    Obtiene el recorrido preorden del árbol (raíz - izquierda - derecha).
    
    Este recorrido visita primero la raíz, luego los descendientes.
    Es útil para copiar o replicar la estructura del árbol.
    
    Orden de visita:
    1. Nodo raíz
    2. Subárbol izquierdo
    3. Subárbol derecho
    
    Returns:
        Lista de niños en orden preorden
    """
    # Obtener recorrido preorden
    return abb_service.get_preorder_traversal()


@router.get("/traversal/postorder", response_model=TraversalResponse)
async def get_postorder_traversal():
    """
    Obtiene el recorrido postorden del árbol (izquierda - derecha - raíz).
    
    Este recorrido visita los hijos antes que la raíz.
    Es útil para eliminar nodos o calcular propiedades de abajo hacia arriba.
    
    Orden de visita:
    1. Subárbol izquierdo
    2. Subárbol derecho
    3. Nodo raíz
    
    Returns:
        Lista de niños en orden postorden
    """
    # Obtener recorrido postorden
    return abb_service.get_postorder_traversal()


# ==================== ENDPOINTS PARA ESTADÍSTICAS ====================

@router.get("/stats")
async def get_tree_statistics():
    """
    Obtiene estadísticas generales del árbol.
    
    Proporciona información útil como:
    - Total de niños en el árbol
    - Si el árbol está vacío
    - Niño en la raíz
    - ID mínimo (niño más a la izquierda)
    - ID máximo (niño más a la derecha)
    
    Returns:
        Diccionario con estadísticas del árbol
    """
    # Obtener estadísticas
    return abb_service.get_tree_stats()


# ==================== ENDPOINTS PARA GESTIÓN DEL ÁRBOL ====================

@router.delete("/tree", response_model=MessageResponse)
async def clear_tree():
    """
    Elimina todos los niños del árbol.
    
    Reinicia el árbol a su estado inicial vacío, eliminando todos los nodos
    y dejando la raíz en None.
    
    Returns:
        Mensaje de confirmación de la operación
    """
    # Obtener el número de niños antes de limpiar
    count_before = abb_service.get_tree_count()
    
    # Limpiar el árbol
    abb_service.clear_tree()
    
    # Retornar mensaje de confirmación
    return MessageResponse(
        message="Árbol limpiado exitosamente",
        details={
            "children_removed": count_before,
            "current_count": 0
        }
    )


@router.get("/tree/count")
async def get_tree_count():
    """
    Obtiene la cantidad total de niños en el árbol.
    
    Returns:
        Diccionario con el número de nodos
    """
    # Obtener el conteo
    count = abb_service.get_tree_count()
    
    # Retornar el resultado
    return {
        "total_children": count,
        "is_empty": count == 0
    }


# ==================== ENDPOINT DE BIENVENIDA ====================

@router.get("/")
async def welcome():
    """
    Endpoint de bienvenida para la API del ABB.
    
    Proporciona información básica sobre los endpoints disponibles.
    
    Returns:
        Diccionario con información de bienvenida
    """
    return {
        "message": "Bienvenido a la API de Árbol Binario de Búsqueda (ABB)",
        "description": "Esta API permite gestionar un ABB de niños con ID, nombre y edad",
        "endpoints": {
            "POST /children": "Agregar un nuevo niño al árbol",
            "GET /children/{id}": "Buscar un niño por su ID",
            "GET /children": "Obtener todos los niños ordenados",
            "GET /tree": "Ver la estructura completa del árbol",
            "GET /traversal/inorder": "Recorrido inorden (orden ascendente)",
            "GET /traversal/preorder": "Recorrido preorden",
            "GET /traversal/postorder": "Recorrido postorden",
            "GET /stats": "Estadísticas del árbol",
            "GET /tree/count": "Cantidad de niños en el árbol",
            "DELETE /tree": "Limpiar el árbol completo"
        },
        "documentation": "/docs para ver la documentación interactiva"
    }
