"""
Script de prueba rapida para verificar que la clase Child con Pydantic funciona correctamente.
"""

from app.models.abb_model import Child, BinarySearchTree

def test_child_creation():
    """Prueba la creacion de un Child con validacion de Pydantic"""
    print("=== Test 1: Creacion de Child valido ===")
    try:
        child = Child(id=1, name="Juan", age=10)
        print(f"[OK] Child creado: {child}")
        print(f"[OK] ID: {child.id}, Nombre: {child.name}, Edad: {child.age}")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
    
    print("\n=== Test 2: Validacion de ID negativo ===")
    try:
        child = Child(id=-1, name="Pedro", age=8)
        print(f"[ERROR] Se creo un Child con ID negativo (no deberia pasar): {child}")
    except Exception as e:
        print(f"[OK] Validacion funciono correctamente: {e}")
    
    print("\n=== Test 3: Validacion de nombre vacio ===")
    try:
        child = Child(id=2, name="", age=9)
        print(f"[ERROR] Se creo un Child con nombre vacio (no deberia pasar): {child}")
    except Exception as e:
        print(f"[OK] Validacion funciono correctamente: {e}")
    
    print("\n=== Test 4: Validacion de edad negativa ===")
    try:
        child = Child(id=3, name="Maria", age=-5)
        print(f"[ERROR] Se creo un Child con edad negativa (no deberia pasar): {child}")
    except Exception as e:
        print(f"[OK] Validacion funciono correctamente: {e}")
    
    print("\n=== Test 5: Validacion de edad mayor a 150 ===")
    try:
        child = Child(id=4, name="Ana", age=200)
        print(f"[ERROR] Se creo un Child con edad > 150 (no deberia pasar): {child}")
    except Exception as e:
        print(f"[OK] Validacion funciono correctamente: {e}")

def test_child_methods():
    """Prueba los metodos de Child"""
    print("\n=== Test 6: Metodos to_dict() y to_response() ===")
    child = Child(id=10, name="Lucas", age=7)
    
    # Probar to_dict()
    child_dict = child.to_dict()
    print(f"[OK] to_dict(): {child_dict}")
    
    # Probar to_response()
    child_response = child.to_response()
    print(f"[OK] to_response(): {child_response}")
    
    print("\n=== Test 7: Metodos __str__, __repr__, __hash__, __eq__ ===")
    child1 = Child(id=5, name="Carlos", age=12)
    child2 = Child(id=5, name="Carlos Jr", age=13)
    child3 = Child(id=6, name="Diana", age=11)
    
    print(f"[OK] __str__: {str(child1)}")
    print(f"[OK] __repr__: {repr(child1)}")
    print(f"[OK] __hash__: {hash(child1)}")
    print(f"[OK] child1 == child2 (mismo ID): {child1 == child2}")
    print(f"[OK] child1 == child3 (diferente ID): {child1 == child3}")

def test_bst_integration():
    """Prueba la integracion de Child con BinarySearchTree"""
    print("\n=== Test 8: Integracion con BinarySearchTree ===")
    
    tree = BinarySearchTree()
    
    # Insertar ninos
    children = [
        Child(id=50, name="Root", age=10),
        Child(id=30, name="Left", age=8),
        Child(id=70, name="Right", age=12),
        Child(id=20, name="LeftLeft", age=6),
        Child(id=40, name="LeftRight", age=9),
    ]
    
    for child in children:
        result = tree.insert(child)
        print(f"[OK] Insertado: {child.name} (ID: {child.id}) - Resultado: {result}")
    
    # Buscar un nino
    print("\n=== Test 9: Busqueda en el arbol ===")
    found = tree.search(30)
    if found:
        print(f"[OK] Nino encontrado: {found}")
    else:
        print("[ERROR] No se encontro el nino")
    
    # Recorrido inorden
    print("\n=== Test 10: Recorrido inorden ===")
    inorder_list = tree.inorder_traversal()
    print("[OK] Recorrido inorden (orden ascendente por ID):")
    for child in inorder_list:
        print(f"  - {child}")
    
    # Estadisticas
    print(f"\n[OK] Total de ninos en el arbol: {tree.get_count()}")
    print(f"[OK] Arbol vacio: {tree.is_empty()}")

def test_pydantic_validation_assignment():
    """Prueba la validacion al asignar valores"""
    print("\n=== Test 11: Validacion al asignar valores (validate_assignment) ===")
    child = Child(id=15, name="Sofia", age=10)
    print(f"[OK] Child inicial: {child}")
    
    try:
        # Intentar asignar un nombre valido
        child.name = "Sofia Maria"
        print(f"[OK] Nombre actualizado: {child.name}")
    except Exception as e:
        print(f"[ERROR] Error al actualizar nombre: {e}")
    
    try:
        # Intentar asignar una edad valida
        child.age = 11
        print(f"[OK] Edad actualizada: {child.age}")
    except Exception as e:
        print(f"[ERROR] Error al actualizar edad: {e}")
    
    try:
        # Intentar asignar un nombre invalido (vacio)
        child.name = ""
        print(f"[ERROR] Se asigno nombre vacio (no deberia pasar): {child.name}")
    except Exception as e:
        print(f"[OK] Validacion en asignacion funciono: {e}")

if __name__ == "__main__":
    print("Iniciando pruebas de Child con Pydantic\n")
    print("=" * 70)
    
    test_child_creation()
    test_child_methods()
    test_bst_integration()
    test_pydantic_validation_assignment()
    
    print("\n" + "=" * 70)
    print("Pruebas completadas")
