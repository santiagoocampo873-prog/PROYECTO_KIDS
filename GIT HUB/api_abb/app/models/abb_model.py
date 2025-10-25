from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum
from app.models.schemas import ChildResponse, TreeNode as TreeNodeSchema


class Gender(str, Enum):
    """Enumeración para los géneros válidos."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Child(BaseModel):
    """
    Clase que representa un niño con sus atributos básicos usando Pydantic.
    Encapsula los datos de cada elemento que se almacenará en el árbol.
    Combina POO con validación automática de datos mediante Pydantic.
    """
    
    # Atributos con validación de Pydantic
    id: int = Field(..., description="ID único del niño (usado como clave del ABB)", gt=0)
    name: str = Field(..., description="Nombre del niño", min_length=1, max_length=100)
    age: int = Field(..., description="Edad del niño", ge=0, le=150)
    city: str = Field(..., description="Ciudad de origen del niño", min_length=1, max_length=100)
    gender: Gender = Field(..., description="Género del niño (male, female, other)")
    
    class Config:
        """
        Configuración de Pydantic para el modelo Child.
        """
        # Permite la validación al asignar valores después de la creación
        validate_assignment = True
        # Previene atributos extra no definidos
        extra = 'forbid'
        # Ejemplo para documentación
        json_schema_extra = {
            "example": {
                "id": 10,
                "name": "Lucas",
                "age": 7,
                "city": "Bogotá",
                "gender": "male"
            }
        }
    
    # Validadores personalizados
    @validator('name')
    def name_must_not_be_empty(cls, v: str) -> str:
        """
        Valida que el nombre no esté vacío después de eliminar espacios.
        
        Args:
            v: Valor del nombre a validar
            
        Returns:
            El nombre validado
            
        Raises:
            ValueError: Si el nombre está vacío
        """
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()
    
    @validator('age')
    def age_must_be_reasonable(cls, v: int) -> int:
        """
        Valida que la edad sea razonable.
        
        Args:
            v: Valor de la edad a validar
            
        Returns:
            La edad validada
            
        Raises:
            ValueError: Si la edad no es válida
        """
        if v < 0:
            raise ValueError('La edad no puede ser negativa')
        if v > 150:
            raise ValueError('La edad no puede ser mayor a 150 años')
        return v
    
    @validator('city')
    def city_must_not_be_empty(cls, v: str) -> str:
        """
        Valida que la ciudad no esté vacía después de eliminar espacios.
        
        Args:
            v: Valor de la ciudad a validar
            
        Returns:
            La ciudad validada
            
        Raises:
            ValueError: Si la ciudad está vacía
        """
        if not v.strip():
            raise ValueError('La ciudad no puede estar vacía')
        return v.strip()
    
    def to_dict(self) -> dict:
        """
        Convierte el objeto Child a un diccionario.
        Útil para serialización y respuestas de la API.
        Utiliza el método dict() nativo de Pydantic.
        
        Returns:
            Diccionario con los datos del niño
        """
        return self.dict()
    
    def to_response(self) -> ChildResponse:
        """
        Convierte el objeto Child a un esquema de respuesta Pydantic.
        Como Child ahora es un modelo Pydantic, puede convertirse directamente.
        
        Returns:
            ChildResponse con los datos del niño
        """
        return ChildResponse(**self.dict())
    
    def __str__(self) -> str:
        """Representación en string del niño para debugging"""
        return f"Child(id={self.id}, name='{self.name}', age={self.age}, city='{self.city}', gender='{self.gender.value}')"
    
    def __repr__(self) -> str:
        """Representación formal del niño"""
        return self.__str__()
    
    def __hash__(self) -> int:
        """
        Permite usar Child como clave en diccionarios o conjuntos.
        Se basa en el ID que es único e inmutable.
        
        Returns:
            Hash basado en el ID del niño
        """
        return hash(self.id)
    
    def __eq__(self, other) -> bool:
        """
        Compara dos objetos Child por su ID.
        
        Args:
            other: Otro objeto a comparar
            
        Returns:
            True si tienen el mismo ID, False en caso contrario
        """
        if not isinstance(other, Child):
            return False
        return self.id == other.id


class Node:
    """
    Clase que representa un nodo del Árbol Binario de Búsqueda.
    Cada nodo contiene un objeto Child y referencias a sus hijos izquierdo y derecho.
    """
    
    def __init__(self, child: Child):
        """
        Constructor de la clase Node.
        
        Args:
            child: Objeto Child que contiene los datos del niño
        """
        # El dato almacenado en este nodo
        self.child = child
        # Referencia al hijo izquierdo (valores menores)
        self.left: Optional[Node] = None
        # Referencia al hijo derecho (valores mayores)
        self.right: Optional[Node] = None
    
    def to_tree_node_schema(self) -> TreeNodeSchema:
        """
        Convierte el nodo y sus hijos a un esquema TreeNode recursivamente.
        Se usa para representar el árbol completo en las respuestas de la API.
        
        Returns:
            TreeNodeSchema con la estructura del nodo y sus descendientes
        """
        return TreeNodeSchema(
            child=self.child.to_response(),
            left=self.left.to_tree_node_schema() if self.left else None,
            right=self.right.to_tree_node_schema() if self.right else None
        )
    
    def __str__(self) -> str:
        """Representación en string del nodo para debugging"""
        return f"Node({self.child})"


class BinarySearchTree:
    """
    Clase que implementa un Árbol Binario de Búsqueda (ABB).
    Permite almacenar niños de forma ordenada por su ID.
    
    Propiedades del ABB:
    - El hijo izquierdo de un nodo tiene un ID menor que el nodo padre
    - El hijo derecho de un nodo tiene un ID mayor que el nodo padre
    - No se permiten IDs duplicados
    """
    
    def __init__(self):
        """
        Constructor de la clase BinarySearchTree.
        Inicializa un árbol vacío con la raíz en None.
        """
        # Raíz del árbol (None si el árbol está vacío)
        self.root: Optional[Node] = None
        # Contador de nodos en el árbol
        self._count: int = 0
    
    def insert(self, child: Child) -> bool:
        """
        Inserta un nuevo niño en el árbol.
        Sigue las reglas del ABB para ubicar el nuevo nodo.
        
        Args:
            child: Objeto Child a insertar
            
        Returns:
            True si se insertó correctamente, False si el ID ya existe
        """
        # Si el árbol está vacío, el nuevo nodo se convierte en la raíz
        if self.root is None:
            self.root = Node(child)
            self._count += 1
            return True
        
        # Si no está vacío, usamos un método auxiliar recursivo
        result = self._insert_recursive(self.root, child)
        if result:
            self._count += 1
        return result
    
    def _insert_recursive(self, current_node: Node, child: Child) -> bool:
        """
        Método auxiliar recursivo para insertar un nodo.
        Navega por el árbol hasta encontrar la posición correcta.
        
        Args:
            current_node: Nodo actual en el recorrido
            child: Objeto Child a insertar
            
        Returns:
            True si se insertó, False si el ID ya existe
        """
        # Si el ID ya existe, no se puede insertar (IDs únicos)
        if child.id == current_node.child.id:
            return False
        
        # Si el ID es menor, debe ir a la izquierda
        if child.id < current_node.child.id:
            # Si no hay hijo izquierdo, insertamos aquí
            if current_node.left is None:
                current_node.left = Node(child)
                return True
            # Si hay hijo izquierdo, continuamos recursivamente
            else:
                return self._insert_recursive(current_node.left, child)
        
        # Si el ID es mayor, debe ir a la derecha
        else:
            # Si no hay hijo derecho, insertamos aquí
            if current_node.right is None:
                current_node.right = Node(child)
                return True
            # Si hay hijo derecho, continuamos recursivamente
            else:
                return self._insert_recursive(current_node.right, child)
    
    def search(self, child_id: int) -> Optional[Child]:
        """
        Busca un niño en el árbol por su ID.
        
        Args:
            child_id: ID del niño a buscar
            
        Returns:
            Objeto Child si se encuentra, None si no existe
        """
        # Usamos el método auxiliar recursivo para buscar
        node = self._search_recursive(self.root, child_id)
        # Retornamos el Child del nodo encontrado, o None
        return node.child if node else None
    
    def _search_recursive(self, current_node: Optional[Node], child_id: int) -> Optional[Node]:
        """
        Método auxiliar recursivo para buscar un nodo por ID.
        
        Args:
            current_node: Nodo actual en el recorrido
            child_id: ID del niño a buscar
            
        Returns:
            Node si se encuentra, None si no existe
        """
        # Caso base: árbol vacío o nodo no encontrado
        if current_node is None:
            return None
        
        # Si encontramos el ID, retornamos el nodo
        if child_id == current_node.child.id:
            return current_node
        
        # Si el ID buscado es menor, buscamos a la izquierda
        if child_id < current_node.child.id:
            return self._search_recursive(current_node.left, child_id)
        
        # Si el ID buscado es mayor, buscamos a la derecha
        else:
            return self._search_recursive(current_node.right, child_id)
    
    def inorder_traversal(self) -> List[Child]:
        """
        Recorrido inorden del árbol (izquierda - raíz - derecha).
        Este recorrido visita los nodos en orden ascendente por ID.
        
        Returns:
            Lista de objetos Child en orden ascendente
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, current_node: Optional[Node], result: List[Child]):
        """
        Método auxiliar recursivo para el recorrido inorden.
        
        Args:
            current_node: Nodo actual en el recorrido
            result: Lista que acumula los resultados
        """
        # Caso base: si el nodo es None, no hacemos nada
        if current_node is None:
            return
        
        # 1. Recorremos el subárbol izquierdo
        self._inorder_recursive(current_node.left, result)
        
        # 2. Visitamos el nodo actual (agregamos el child a la lista)
        result.append(current_node.child)
        
        # 3. Recorremos el subárbol derecho
        self._inorder_recursive(current_node.right, result)
    
    def preorder_traversal(self) -> List[Child]:
        """
        Recorrido preorden del árbol (raíz - izquierda - derecha).
        Este recorrido visita primero la raíz, luego los hijos.
        
        Returns:
            Lista de objetos Child en orden preorden
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, current_node: Optional[Node], result: List[Child]):
        """
        Método auxiliar recursivo para el recorrido preorden.
        
        Args:
            current_node: Nodo actual en el recorrido
            result: Lista que acumula los resultados
        """
        # Caso base: si el nodo es None, no hacemos nada
        if current_node is None:
            return
        
        # 1. Visitamos el nodo actual primero
        result.append(current_node.child)
        
        # 2. Recorremos el subárbol izquierdo
        self._preorder_recursive(current_node.left, result)
        
        # 3. Recorremos el subárbol derecho
        self._preorder_recursive(current_node.right, result)
    
    def postorder_traversal(self) -> List[Child]:
        """
        Recorrido postorden del árbol (izquierda - derecha - raíz).
        Este recorrido visita los hijos antes que la raíz.
        
        Returns:
            Lista de objetos Child en orden postorden
        """
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, current_node: Optional[Node], result: List[Child]):
        """
        Método auxiliar recursivo para el recorrido postorden.
        
        Args:
            current_node: Nodo actual en el recorrido
            result: Lista que acumula los resultados
        """
        # Caso base: si el nodo es None, no hacemos nada
        if current_node is None:
            return
        
        # 1. Recorremos el subárbol izquierdo
        self._postorder_recursive(current_node.left, result)
        
        # 2. Recorremos el subárbol derecho
        self._postorder_recursive(current_node.right, result)
        
        # 3. Visitamos el nodo actual al final
        result.append(current_node.child)
    
    def get_count(self) -> int:
        """
        Retorna la cantidad total de nodos en el árbol.
        
        Returns:
            Número de niños almacenados en el árbol
        """
        return self._count
    
    def is_empty(self) -> bool:
        """
        Verifica si el árbol está vacío.
        
        Returns:
            True si no hay nodos, False si hay al menos uno
        """
        return self.root is None
    
    def clear(self):
        """
        Elimina todos los nodos del árbol.
        Reinicia el árbol a su estado inicial vacío.
        """
        self.root = None
        self._count = 0
    
    def to_tree_schema(self) -> Optional[TreeNodeSchema]:
        """
        Convierte el árbol completo a un esquema TreeNode.
        Se usa para representar el árbol en las respuestas de la API.
        
        Returns:
            TreeNodeSchema con la estructura completa del árbol, o None si está vacío
        """
        if self.root is None:
            return None
        return self.root.to_tree_node_schema()
