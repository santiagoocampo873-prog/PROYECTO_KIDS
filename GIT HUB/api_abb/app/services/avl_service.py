from typing import List, Optional
from app.models.avl_model import AVLTree, Child
from app.models.schemas import (
    ChildCreate, 
    ChildResponse, 
    TreeResponse, 
    TraversalResponse
)


class AVLService:
    """
    Servicio que encapsula la lógica de negocio del Árbol AVL.
    Actúa como intermediario entre el controlador y el modelo del AVL.
    Sigue el principio de separación de responsabilidades (Single Responsibility Principle).
    """
    
    def __init__(self):
        """
        Constructor del servicio AVL.
        Inicializa una instancia única del árbol AVL auto-balanceado.
        """
        # Instancia única del árbol que se mantiene en memoria
        self._tree = AVLTree()
    
    def add_child(self, child_data: ChildCreate) -> dict:
        """
        Agrega un nuevo niño al árbol AVL.
        El árbol se auto-balancea después de la inserción.
        Valida que el ID no exista antes de insertar.
        
        Args:
            child_data: Datos del niño a agregar (ChildCreate schema)
            
        Returns:
            Diccionario con el resultado de la operación:
            - success: True si se insertó, False si el ID ya existe
            - message: Mensaje descriptivo del resultado
            - child: Datos del niño insertado (si fue exitoso)
            - balanced: Indica si el árbol quedó balanceado (siempre True en AVL)
        """
        # Crear objeto Child desde los datos recibidos
        child = Child(
            id=child_data.id,
            name=child_data.name,
            age=child_data.age
        )
        
        # Intentar insertar el niño en el árbol
        success = self._tree.insert(child)
        
        # Si la inserción fue exitosa
        if success:
            return {
                "success": True,
                "message": f"Niño '{child.name}' con ID {child.id} agregado exitosamente al árbol AVL",
                "child": child.to_response(),
                "balanced": self._tree.is_balanced(),
                "tree_height": self._tree.get_tree_height()
            }
        # Si el ID ya existe (inserción fallida)
        else:
            return {
                "success": False,
                "message": f"No se puede agregar el niño. El ID {child.id} ya existe en el árbol",
                "child": None
            }
    
    def search_child(self, child_id: int) -> Optional[ChildResponse]:
        """
        Busca un niño en el árbol por su ID.
        
        Args:
            child_id: ID del niño a buscar
            
        Returns:
            ChildResponse con los datos del niño si existe, None si no se encuentra
        """
        # Buscar el niño en el árbol
        child = self._tree.search(child_id)
        
        # Si se encontró, convertir a schema de respuesta
        if child:
            return child.to_response()
        
        # Si no se encontró, retornar None
        return None
    
    def get_tree_structure(self) -> TreeResponse:
        """
        Obtiene la estructura completa del árbol AVL.
        Útil para visualizar el árbol de forma jerárquica y verificar el balance.
        
        Returns:
            TreeResponse con la estructura del árbol y el conteo total de nodos
        """
        # Obtener la representación del árbol en formato schema
        tree_schema = self._tree.to_tree_schema()
        
        # Retornar la respuesta con el árbol y el total de niños
        return TreeResponse(
            root=tree_schema,
            total_children=self._tree.get_count()
        )
    
    def get_inorder_traversal(self) -> TraversalResponse:
        """
        Obtiene el recorrido inorden del árbol.
        Los niños se retornan ordenados por ID de menor a mayor.
        
        Returns:
            TraversalResponse con el tipo de recorrido y la lista de niños ordenados
        """
        # Realizar el recorrido inorden
        children = self._tree.inorder_traversal()
        
        # Convertir cada Child a ChildResponse
        children_response = [child.to_response() for child in children]
        
        # Retornar la respuesta con el tipo y los datos
        return TraversalResponse(
            traversal_type="inorden (izquierda - raíz - derecha)",
            children=children_response
        )
    
    def get_preorder_traversal(self) -> TraversalResponse:
        """
        Obtiene el recorrido preorden del árbol.
        Se visita primero la raíz, luego el subárbol izquierdo, luego el derecho.
        
        Returns:
            TraversalResponse con el tipo de recorrido y la lista de niños
        """
        # Realizar el recorrido preorden
        children = self._tree.preorder_traversal()
        
        # Convertir cada Child a ChildResponse
        children_response = [child.to_response() for child in children]
        
        # Retornar la respuesta con el tipo y los datos
        return TraversalResponse(
            traversal_type="preorden (raíz - izquierda - derecha)",
            children=children_response
        )
    
    def get_postorder_traversal(self) -> TraversalResponse:
        """
        Obtiene el recorrido postorden del árbol.
        Se visitan los hijos antes que la raíz.
        
        Returns:
            TraversalResponse con el tipo de recorrido y la lista de niños
        """
        # Realizar el recorrido postorden
        children = self._tree.postorder_traversal()
        
        # Convertir cada Child a ChildResponse
        children_response = [child.to_response() for child in children]
        
        # Retornar la respuesta con el tipo y los datos
        return TraversalResponse(
            traversal_type="postorden (izquierda - derecha - raíz)",
            children=children_response
        )
    
    def get_all_children(self) -> List[ChildResponse]:
        """
        Obtiene todos los niños del árbol en orden ascendente por ID.
        Utiliza el recorrido inorden para retornar los datos ordenados.
        
        Returns:
            Lista de ChildResponse ordenada por ID
        """
        # Obtener los niños mediante recorrido inorden (orden ascendente)
        children = self._tree.inorder_traversal()
        
        # Convertir cada Child a ChildResponse
        return [child.to_response() for child in children]
    
    def get_tree_count(self) -> int:
        """
        Obtiene el número total de niños en el árbol.
        
        Returns:
            Cantidad de nodos en el árbol
        """
        return self._tree.get_count()
    
    def is_tree_empty(self) -> bool:
        """
        Verifica si el árbol está vacío.
        
        Returns:
            True si el árbol no tiene nodos, False en caso contrario
        """
        return self._tree.is_empty()
    
    def clear_tree(self):
        """
        Elimina todos los nodos del árbol.
        Reinicia el árbol a su estado inicial vacío.
        """
        self._tree.clear()
    
    def get_tree_stats(self) -> dict:
        """
        Obtiene estadísticas generales del árbol AVL.
        Incluye información específica del AVL como altura y estado de balance.
        
        Returns:
            Diccionario con información estadística del árbol
        """
        # Verificar si el árbol está vacío
        is_empty = self._tree.is_empty()
        
        # Si está vacío, retornar estadísticas vacías
        if is_empty:
            return {
                "total_children": 0,
                "is_empty": True,
                "root_child": None,
                "min_id": None,
                "max_id": None,
                "tree_height": 0,
                "is_balanced": True
            }
        
        # Obtener todos los niños
        all_children = self._tree.inorder_traversal()
        
        # El recorrido inorden está ordenado, el primero es el mínimo y el último el máximo
        min_child = all_children[0] if all_children else None
        max_child = all_children[-1] if all_children else None
        
        # Obtener el niño en la raíz
        root_child = self._tree.root.child if self._tree.root else None
        
        # Retornar estadísticas incluyendo información específica del AVL
        return {
            "total_children": self._tree.get_count(),
            "is_empty": False,
            "root_child": root_child.to_response() if root_child else None,
            "min_id": min_child.id if min_child else None,
            "max_id": max_child.id if max_child else None,
            "tree_height": self._tree.get_tree_height(),
            "is_balanced": self._tree.is_balanced()
        }
    
    def check_balance(self) -> dict:
        """
        Verifica el estado de balance del árbol AVL.
        Un árbol AVL siempre debe estar balanceado.
        
        Returns:
            Diccionario con información sobre el balance del árbol
        """
        is_balanced = self._tree.is_balanced()
        height = self._tree.get_tree_height()
        
        return {
            "is_balanced": is_balanced,
            "tree_height": height,
            "total_children": self._tree.get_count(),
            "message": "El árbol AVL está correctamente balanceado" if is_balanced 
                      else "ADVERTENCIA: El árbol NO está balanceado"
        }


# Instancia única del servicio (patrón Singleton)
# Esta instancia se usará en todos los endpoints
avl_service = AVLService()
