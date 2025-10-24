from pydantic import BaseModel, Field
from typing import Optional, List


# ========== ESQUEMAS PARA NIÑO (CHILD) ==========

class ChildCreate(BaseModel):
    """
    Esquema para crear un niño nuevo en el árbol.
    Contiene los datos necesarios para agregar un nodo al ABB.
    """
    id: int = Field(..., description="ID único del niño (usado como clave del ABB)", gt=0)
    name: str = Field(..., description="Nombre del niño", min_length=1, max_length=100)
    age: int = Field(..., description="Edad del niño", ge=0, le=150)

    class Config:
        # Ejemplo para documentación de la API
        json_schema_extra = {
            "example": {
                "id": 10,
                "name": "Lucas",
                "age": 7
            }
        }


class ChildResponse(BaseModel):
    """
    Esquema de respuesta que representa un niño.
    Se usa para devolver datos de un niño desde el árbol.
    """
    id: int = Field(..., description="ID único del niño")
    name: str = Field(..., description="Nombre del niño")
    age: int = Field(..., description="Edad del niño")

    class Config:
        # Ejemplo para documentación de la API
        json_schema_extra = {
            "example": {
                "id": 10,
                "name": "Lucas",
                "age": 7
            }
        }


# ========== ESQUEMAS PARA RESPUESTAS DEL ÁRBOL ==========

class TreeNode(BaseModel):
    """
    Esquema que representa un nodo del árbol en formato visual.
    Incluye el niño y sus hijos izquierdo y derecho.
    """
    child: ChildResponse = Field(..., description="Datos del niño en este nodo")
    left: Optional['TreeNode'] = Field(None, description="Hijo izquierdo (valores menores)")
    right: Optional['TreeNode'] = Field(None, description="Hijo derecho (valores mayores)")


class TreeResponse(BaseModel):
    """
    Esquema de respuesta para visualizar el árbol completo.
    """
    root: Optional[TreeNode] = Field(None, description="Nodo raíz del árbol")
    total_children: int = Field(..., description="Cantidad total de niños en el árbol")


class TraversalResponse(BaseModel):
    """
    Esquema de respuesta para los diferentes tipos de recorrido del árbol.
    """
    traversal_type: str = Field(..., description="Tipo de recorrido realizado")
    children: List[ChildResponse] = Field(..., description="Lista de niños en el orden del recorrido")


class MessageResponse(BaseModel):
    """
    Esquema para respuestas con mensajes simples.
    """
    message: str = Field(..., description="Mensaje de respuesta")
    details: Optional[dict] = Field(None, description="Detalles adicionales opcionales")


# ========== CONFIGURACIÓN PARA REFERENCIAS CIRCULARES ==========

# Actualizar referencias para permitir el anidamiento recursivo de TreeNode
# En Pydantic v1 se usa update_forward_refs() en lugar de model_rebuild()
TreeNode.update_forward_refs()
