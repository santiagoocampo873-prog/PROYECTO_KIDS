from typing import Optional, List
from app.models.schemas import ChildResponse, TreeNode as TreeNodeSchema


class Child:
    """
    Clase que representa un niño con sus atributos básicos.
    Encapsula los datos de cada elemento que se almacenará en el árbol AVL.
    """
    
    def __init__(self, id: int, name: str, age: int):
        """
        Constructor de la clase Child.
        
        Args:
            id: Identificador único del niño (se usa como clave en el AVL)
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


class AVLNode:
    """
    Clase que representa un nodo del Árbol AVL.
    A diferencia de un nodo normal de ABB, este nodo mantiene la altura del subárbol.
    """
    
    def __init__(self, child: Child):
        """
        Constructor de la clase AVLNode.
        
        Args:
            child: Objeto Child que contiene los datos del niño
        """
        # El dato almacenado en este nodo
        self.child = child
        # Referencia al hijo izquierdo (valores menores)
        self.left: Optional[AVLNode] = None
        # Referencia al hijo derecho (valores mayores)
        self.right: Optional[AVLNode] = None
        # Altura del nodo (importante para el balanceo AVL)
        self.height: int = 1
    
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
        return f"AVLNode({self.child}, height={self.height})"


class AVLTree:
    """
    Clase que implementa un Árbol AVL (Adelson-Velsky and Landis).
    Es un ABB auto-balanceado que mantiene la propiedad de que la diferencia
    de alturas entre los subárboles izquierdo y derecho nunca es mayor a 1.
    
    Propiedades del AVL:
    - Es un ABB: valores izquierda < raíz < valores derecha
    - Está balanceado: |altura(izq) - altura(der)| <= 1 para cada nodo
    - Se auto-balancea mediante rotaciones después de cada inserción
    """
    
    def __init__(self):
        """
        Constructor de la clase AVLTree.
        Inicializa un árbol vacío con la raíz en None.
        """
        # Raíz del árbol (None si el árbol está vacío)
        self.root: Optional[AVLNode] = None
        # Contador de nodos en el árbol
        self._count: int = 0
    
    def _get_height(self, node: Optional[AVLNode]) -> int:
        """
        Obtiene la altura de un nodo.
        La altura de None es 0, la de una hoja es 1.
        
        Args:
            node: Nodo del cual obtener la altura
            
        Returns:
            Altura del nodo (0 si es None)
        """
        # Si el nodo es None, su altura es 0
        if node is None:
            return 0
        # Si no, retornar la altura almacenada
        return node.height
    
    def _update_height(self, node: AVLNode):
        """
        Actualiza la altura de un nodo basándose en las alturas de sus hijos.
        La altura de un nodo es 1 + el máximo de las alturas de sus hijos.
        
        Args:
            node: Nodo cuya altura se va a actualizar
        """
        # La altura es 1 más el máximo de las alturas de los hijos
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
    
    def _get_balance_factor(self, node: Optional[AVLNode]) -> int:
        """
        Calcula el factor de balance de un nodo.
        Factor de balance = altura(izquierda) - altura(derecha)
        
        Un nodo está balanceado si su factor de balance está entre -1 y 1.
        
        Args:
            node: Nodo del cual calcular el factor de balance
            
        Returns:
            Factor de balance del nodo (0 si el nodo es None)
        """
        # Si el nodo es None, su factor de balance es 0
        if node is None:
            return 0
        # Calcular: altura izquierda - altura derecha
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _rotate_right(self, z: AVLNode) -> AVLNode:
        """
        Realiza una rotación simple a la derecha.
        
        Se usa cuando el subárbol izquierdo es más alto (balance > 1).
        
        Transformación:
              z                y
             / \              / \
            y   C    -->     x   z
           / \                  / \
          x   B                B   C
        
        Args:
            z: Nodo raíz de la rotación
            
        Returns:
            Nueva raíz después de la rotación (nodo y)
        """
        # Guardar referencias a los nodos involucrados
        y = z.left  # y será la nueva raíz
        B = y.right  # B es el subárbol derecho de y
        
        # Realizar la rotación
        y.right = z  # z se convierte en hijo derecho de y
        z.left = B   # B se convierte en hijo izquierdo de z
        
        # Actualizar alturas (primero z, luego y)
        self._update_height(z)
        self._update_height(y)
        
        # Retornar la nueva raíz
        return y
    
    def _rotate_left(self, z: AVLNode) -> AVLNode:
        """
        Realiza una rotación simple a la izquierda.
        
        Se usa cuando el subárbol derecho es más alto (balance < -1).
        
        Transformación:
            z                  y
           / \                / \
          A   y      -->     z   x
             / \            / \
            B   x          A   B
        
        Args:
            z: Nodo raíz de la rotación
            
        Returns:
            Nueva raíz después de la rotación (nodo y)
        """
        # Guardar referencias a los nodos involucrados
        y = z.right  # y será la nueva raíz
        B = y.left   # B es el subárbol izquierdo de y
        
        # Realizar la rotación
        y.left = z   # z se convierte en hijo izquierdo de y
        z.right = B  # B se convierte en hijo derecho de z
        
        # Actualizar alturas (primero z, luego y)
        self._update_height(z)
        self._update_height(y)
        
        # Retornar la nueva raíz
        return y
    
    def _rebalance(self, node: AVLNode) -> AVLNode:
        """
        Rebalancea un nodo si es necesario mediante rotaciones.
        
        Hay 4 casos de desbalance:
        1. Izquierda-Izquierda (LL): rotación derecha simple
        2. Derecha-Derecha (RR): rotación izquierda simple
        3. Izquierda-Derecha (LR): rotación izquierda en hijo, luego derecha
        4. Derecha-Izquierda (RL): rotación derecha en hijo, luego izquierda
        
        Args:
            node: Nodo a rebalancear
            
        Returns:
            Nueva raíz del subárbol rebalanceado
        """
        # Actualizar la altura del nodo actual
        self._update_height(node)
        
        # Calcular el factor de balance
        balance = self._get_balance_factor(node)
        
        # Caso 1: Desbalance Izquierda-Izquierda (LL)
        # El subárbol izquierdo es más alto y el problema está en la izquierda del hijo izquierdo
        if balance > 1 and self._get_balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        
        # Caso 2: Desbalance Derecha-Derecha (RR)
        # El subárbol derecho es más alto y el problema está en la derecha del hijo derecho
        if balance < -1 and self._get_balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        
        # Caso 3: Desbalance Izquierda-Derecha (LR)
        # El subárbol izquierdo es más alto y el problema está en la derecha del hijo izquierdo
        if balance > 1 and self._get_balance_factor(node.left) < 0:
            # Primero rotación izquierda en el hijo izquierdo
            node.left = self._rotate_left(node.left)
            # Luego rotación derecha en el nodo actual
            return self._rotate_right(node)
        
        # Caso 4: Desbalance Derecha-Izquierda (RL)
        # El subárbol derecho es más alto y el problema está en la izquierda del hijo derecho
        if balance < -1 and self._get_balance_factor(node.right) > 0:
            # Primero rotación derecha en el hijo derecho
            node.right = self._rotate_right(node.right)
            # Luego rotación izquierda en el nodo actual
            return self._rotate_left(node)
        
        # Si el nodo está balanceado, retornarlo sin cambios
        return node
    
    def insert(self, child: Child) -> bool:
        """
        Inserta un nuevo niño en el árbol AVL.
        Después de insertar, el árbol se auto-balancea si es necesario.
        
        Args:
            child: Objeto Child a insertar
            
        Returns:
            True si se insertó correctamente, False si el ID ya existe
        """
        # Intentar insertar el nodo
        result, self.root = self._insert_recursive(self.root, child)
        
        # Si la inserción fue exitosa, incrementar el contador
        if result:
            self._count += 1
        
        return result
    
    def _insert_recursive(self, node: Optional[AVLNode], child: Child) -> tuple[bool, Optional[AVLNode]]:
        """
        Método auxiliar recursivo para insertar un nodo y rebalancear.
        
        Args:
            node: Nodo actual en el recorrido
            child: Objeto Child a insertar
            
        Returns:
            Tupla (éxito, nodo_raíz_actualizado)
        """
        # Caso base: encontramos el lugar para insertar
        if node is None:
            return True, AVLNode(child)
        
        # Si el ID ya existe, no insertar
        if child.id == node.child.id:
            return False, node
        
        # Insertar recursivamente según el valor del ID
        if child.id < node.child.id:
            # Insertar en el subárbol izquierdo
            success, node.left = self._insert_recursive(node.left, child)
        else:
            # Insertar en el subárbol derecho
            success, node.right = self._insert_recursive(node.right, child)
        
        # Si la inserción falló, retornar sin rebalancear
        if not success:
            return False, node
        
        # Rebalancear el nodo después de la inserción
        node = self._rebalance(node)
        
        return True, node
    
    def search(self, child_id: int) -> Optional[Child]:
        """
        Busca un niño en el árbol por su ID.
        La búsqueda en un AVL es igual que en un ABB.
        
        Args:
            child_id: ID del niño a buscar
            
        Returns:
            Objeto Child si se encuentra, None si no existe
        """
        # Usar el método auxiliar recursivo para buscar
        node = self._search_recursive(self.root, child_id)
        # Retornar el Child del nodo encontrado, o None
        return node.child if node else None
    
    def _search_recursive(self, node: Optional[AVLNode], child_id: int) -> Optional[AVLNode]:
        """
        Método auxiliar recursivo para buscar un nodo por ID.
        
        Args:
            node: Nodo actual en el recorrido
            child_id: ID del niño a buscar
            
        Returns:
            AVLNode si se encuentra, None si no existe
        """
        # Caso base: árbol vacío o nodo no encontrado
        if node is None:
            return None
        
        # Si encontramos el ID, retornar el nodo
        if child_id == node.child.id:
            return node
        
        # Si el ID buscado es menor, buscar a la izquierda
        if child_id < node.child.id:
            return self._search_recursive(node.left, child_id)
        
        # Si el ID buscado es mayor, buscar a la derecha
        else:
            return self._search_recursive(node.right, child_id)
    
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
    
    def _inorder_recursive(self, node: Optional[AVLNode], result: List[Child]):
        """
        Método auxiliar recursivo para el recorrido inorden.
        
        Args:
            node: Nodo actual en el recorrido
            result: Lista que acumula los resultados
        """
        # Caso base: si el nodo es None, no hacemos nada
        if node is None:
            return
        
        # 1. Recorremos el subárbol izquierdo
        self._inorder_recursive(node.left, result)
        
        # 2. Visitamos el nodo actual (agregamos el child a la lista)
        result.append(node.child)
        
        # 3. Recorremos el subárbol derecho
        self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self) -> List[Child]:
        """
        Recorrido preorden del árbol (raíz - izquierda - derecha).
        Este recorrido visita primero la raíz, luego los descendientes.
        
        Returns:
            Lista de objetos Child en orden preorden
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node: Optional[AVLNode], result: List[Child]):
        """
        Método auxiliar recursivo para el recorrido preorden.
        
        Args:
            node: Nodo actual en el recorrido
            result: Lista que acumula los resultados
        """
        # Caso base: si el nodo es None, no hacemos nada
        if node is None:
            return
        
        # 1. Visitamos el nodo actual primero
        result.append(node.child)
        
        # 2. Recorremos el subárbol izquierdo
        self._preorder_recursive(node.left, result)
        
        # 3. Recorremos el subárbol derecho
        self._preorder_recursive(node.right, result)
    
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
    
    def _postorder_recursive(self, node: Optional[AVLNode], result: List[Child]):
        """
        Método auxiliar recursivo para el recorrido postorden.
        
        Args:
            node: Nodo actual en el recorrido
            result: Lista que acumula los resultados
        """
        # Caso base: si el nodo es None, no hacemos nada
        if node is None:
            return
        
        # 1. Recorremos el subárbol izquierdo
        self._postorder_recursive(node.left, result)
        
        # 2. Recorremos el subárbol derecho
        self._postorder_recursive(node.right, result)
        
        # 3. Visitamos el nodo actual al final
        result.append(node.child)
    
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
    
    def get_tree_height(self) -> int:
        """
        Obtiene la altura del árbol completo.
        La altura del árbol es la altura de la raíz.
        
        Returns:
            Altura del árbol (0 si está vacío)
        """
        return self._get_height(self.root)
    
    def is_balanced(self) -> bool:
        """
        Verifica si el árbol está balanceado (propiedad AVL).
        Un árbol AVL siempre debería estar balanceado.
        
        Returns:
            True si está balanceado, False en caso contrario
        """
        return self._check_balanced(self.root)
    
    def _check_balanced(self, node: Optional[AVLNode]) -> bool:
        """
        Método auxiliar recursivo para verificar el balance del árbol.
        
        Args:
            node: Nodo actual a verificar
            
        Returns:
            True si el subárbol está balanceado
        """
        # Un árbol vacío está balanceado
        if node is None:
            return True
        
        # Verificar que el factor de balance esté entre -1 y 1
        balance = self._get_balance_factor(node)
        if abs(balance) > 1:
            return False
        
        # Verificar recursivamente los subárboles
        return self._check_balanced(node.left) and self._check_balanced(node.right)
    
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
