from typing import Optional, List
from app.models.schemas import ChildResponse, TreeNode as TreeNodeSchema


class Child:
    """
    Clase que representa un niño con sus atributos básicos.
    Encapsula los datos de cada elemento que se almacenará en el árbol.
    """
    
    def __init__(self, id: int, name: str, age: int):
        """
        Constructor de la clase Child.
        
        Args:
            id: Identificador único del niño (se usa como clave en el ABB)
            name: Nombre del niño
            age: Edad del niño
        """
        # Atributos privados siguiendo el principio de encapsulamiento
        self._id = id
        self._name = name
        self._age = age
    
    # Propiedades (getters) para acceder a los atributos privados
    @property
    def id(self) -> int:
        """Retorna el ID del niño"""
        return self._id
    
    @property
    def name(self) -> str:
        """Retorna el nombre del niño"""
        return self._name
    
    @property
    def age(self) -> int:
        """Retorna la edad del niño"""
        return self._age
    
    # Setters para modificar los atributos (excepto el ID que es inmutable)
    @name.setter
    def name(self, value: str):
        """Establece el nombre del niño"""
        self._name = value
    
    @age.setter
    def age(self, value: int):
        """Establece la edad del niño"""
        self._age = value
    
    def to_dict(self) -> dict:
        """
        Convierte el objeto Child a un diccionario.
        Útil para serialización y respuestas de la API.
        
        Returns:
            Diccionario con los datos del niño
        """
        return {
            "id": self._id,
            "name": self._name,
            "age": self._age
        }
    
    def to_response(self) -> ChildResponse:
        """
        Convierte el objeto Child a un esquema de respuesta Pydantic.
        
        Returns:
            ChildResponse con los datos del niño
        """
        return ChildResponse(id=self._id, name=self._name, age=self._age)
    
    def __str__(self) -> str:
        """Representación en string del niño para debugging"""
        return f"Child(id={self._id}, name='{self._name}', age={self._age})"
    
    def __repr__(self) -> str:
        """Representación formal del niño"""
        return self.__str__()


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
