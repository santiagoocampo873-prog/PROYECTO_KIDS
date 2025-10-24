from typing import List, Optional
from app.models.schemas import ExampleCreate, ExampleUpdate, ExampleResponse


class ExampleService:
    """
    Servicio para manejar la lógica de negocio de Examples.
    Demuestra el principio de separación de responsabilidades (Single Responsibility).
    """
    
    def __init__(self):
        """
        Constructor del servicio.
        En un caso real, aquí se inyectaría la dependencia de la base de datos.
        """
        # Simulación de almacenamiento en memoria
        self._storage: List[dict] = []
        self._next_id: int = 1
    
    def create(self, example_data: ExampleCreate) -> ExampleResponse:
        """
        Crea un nuevo ejemplo.
        
        Args:
            example_data: Datos del ejemplo a crear
            
        Returns:
            ExampleResponse con el ejemplo creado
        """
        example_dict = example_data.dict()
        example_dict["id"] = self._next_id
        self._next_id += 1
        
        self._storage.append(example_dict)
        return ExampleResponse(**example_dict)
    
    def get_all(self) -> List[ExampleResponse]:
        """
        Obtiene todos los ejemplos.
        
        Returns:
            Lista de ExampleResponse
        """
        return [ExampleResponse(**item) for item in self._storage]
    
    def get_by_id(self, example_id: int) -> Optional[ExampleResponse]:
        """
        Obtiene un ejemplo por su ID.
        
        Args:
            example_id: ID del ejemplo a buscar
            
        Returns:
            ExampleResponse si se encuentra, None en caso contrario
        """
        for item in self._storage:
            if item["id"] == example_id:
                return ExampleResponse(**item)
        return None
    
    def update(self, example_id: int, example_data: ExampleUpdate) -> Optional[ExampleResponse]:
        """
        Actualiza un ejemplo existente.
        
        Args:
            example_id: ID del ejemplo a actualizar
            example_data: Datos a actualizar
            
        Returns:
            ExampleResponse actualizado si se encuentra, None en caso contrario
        """
        for item in self._storage:
            if item["id"] == example_id:
                update_data = example_data.dict(exclude_unset=True)
                item.update(update_data)
                return ExampleResponse(**item)
        return None
    
    def delete(self, example_id: int) -> bool:
        """
        Elimina un ejemplo.
        
        Args:
            example_id: ID del ejemplo a eliminar
            
        Returns:
            True si se eliminó, False si no se encontró
        """
        for i, item in enumerate(self._storage):
            if item["id"] == example_id:
                self._storage.pop(i)
                return True
        return False


# Instancia singleton del servicio
example_service = ExampleService()
