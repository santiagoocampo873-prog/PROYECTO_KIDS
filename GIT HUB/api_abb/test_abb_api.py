"""
Script de prueba para la API del Árbol Binario de Búsqueda.
Este script demuestra todas las funcionalidades de la API.
"""

import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000/abb"

# Colores para output en consola
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'


def print_success(message):
    """Imprime un mensaje de éxito en verde"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message):
    """Imprime un mensaje de error en rojo"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message):
    """Imprime un mensaje informativo en azul"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")


def print_section(title):
    """Imprime un título de sección"""
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}\n")


def test_add_child(id, name, age):
    """
    Prueba agregar un niño al árbol.
    
    Args:
        id: ID del niño
        name: Nombre del niño
        age: Edad del niño
    """
    print_info(f"Agregando niño: ID={id}, Nombre={name}, Edad={age}")
    
    # Datos del niño
    child_data = {
        "id": id,
        "name": name,
        "age": age
    }
    
    try:
        # Hacer la petición POST
        response = requests.post(f"{BASE_URL}/children", json=child_data)
        
        # Verificar el resultado
        if response.status_code == 201:
            result = response.json()
            print_success(f"Niño agregado exitosamente: {result['message']}")
            return True
        elif response.status_code == 409:
            error = response.json()
            print_error(f"ID duplicado: {error['detail']}")
            return False
        else:
            print_error(f"Error inesperado: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False


def test_get_child(child_id):
    """
    Prueba buscar un niño por ID.
    
    Args:
        child_id: ID del niño a buscar
    """
    print_info(f"Buscando niño con ID={child_id}")
    
    try:
        # Hacer la petición GET
        response = requests.get(f"{BASE_URL}/children/{child_id}")
        
        # Verificar el resultado
        if response.status_code == 200:
            child = response.json()
            print_success(f"Niño encontrado: {json.dumps(child, indent=2, ensure_ascii=False)}")
            return child
        elif response.status_code == 404:
            print_error(f"Niño con ID {child_id} no encontrado")
            return None
        else:
            print_error(f"Error inesperado: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None


def test_get_all_children():
    """Prueba obtener todos los niños ordenados"""
    print_info("Obteniendo todos los niños (ordenados por ID)")
    
    try:
        # Hacer la petición GET
        response = requests.get(f"{BASE_URL}/children")
        
        # Verificar el resultado
        if response.status_code == 200:
            children = response.json()
            print_success(f"Total de niños: {len(children)}")
            print(json.dumps(children, indent=2, ensure_ascii=False))
            return children
        else:
            print_error(f"Error: {response.status_code}")
            return []
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return []


def test_get_tree_structure():
    """Prueba obtener la estructura del árbol"""
    print_info("Obteniendo estructura del árbol")
    
    try:
        # Hacer la petición GET
        response = requests.get(f"{BASE_URL}/tree")
        
        # Verificar el resultado
        if response.status_code == 200:
            tree = response.json()
            print_success(f"Árbol obtenido. Total de niños: {tree['total_children']}")
            print(json.dumps(tree, indent=2, ensure_ascii=False))
            return tree
        else:
            print_error(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None


def test_traversal(traversal_type):
    """
    Prueba un tipo de recorrido del árbol.
    
    Args:
        traversal_type: Tipo de recorrido (inorder, preorder, postorder)
    """
    print_info(f"Obteniendo recorrido {traversal_type}")
    
    try:
        # Hacer la petición GET
        response = requests.get(f"{BASE_URL}/traversal/{traversal_type}")
        
        # Verificar el resultado
        if response.status_code == 200:
            result = response.json()
            print_success(f"Recorrido: {result['traversal_type']}")
            print(json.dumps(result['children'], indent=2, ensure_ascii=False))
            return result
        else:
            print_error(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None


def test_get_stats():
    """Prueba obtener estadísticas del árbol"""
    print_info("Obteniendo estadísticas del árbol")
    
    try:
        # Hacer la petición GET
        response = requests.get(f"{BASE_URL}/stats")
        
        # Verificar el resultado
        if response.status_code == 200:
            stats = response.json()
            print_success("Estadísticas obtenidas:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
            return stats
        else:
            print_error(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None


def test_clear_tree():
    """Prueba limpiar el árbol completo"""
    print_info("Limpiando el árbol completo")
    
    try:
        # Hacer la petición DELETE
        response = requests.delete(f"{BASE_URL}/tree")
        
        # Verificar el resultado
        if response.status_code == 200:
            result = response.json()
            print_success(f"{result['message']}")
            print(f"Detalles: {json.dumps(result['details'], indent=2, ensure_ascii=False)}")
            return True
        else:
            print_error(f"Error: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False


def main():
    """Función principal que ejecuta todas las pruebas"""
    
    print_section("PRUEBA COMPLETA DE LA API DEL ABB")
    
    # Verificar que la API esté activa
    print_info("Verificando conexión con la API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success("Conexión exitosa con la API")
        else:
            print_error("La API no está respondiendo correctamente")
            return
    except Exception as e:
        print_error(f"No se puede conectar a la API: {e}")
        print_info("Asegúrate de que la API esté corriendo: uvicorn app.main:app --reload")
        return
    
    # 1. Agregar niños (ejemplo del documento ABB.md)
    print_section("1. AGREGAR NIÑOS AL ÁRBOL")
    test_add_child(10, "Lucas", 7)      # Será la raíz
    test_add_child(6, "Sofía", 5)       # Irá a la izquierda
    test_add_child(15, "Mateo", 8)      # Irá a la derecha
    test_add_child(4, "Valentina", 6)   # Irá a la izquierda de Sofía
    
    # 2. Intentar agregar ID duplicado
    print_section("2. PROBAR ID DUPLICADO")
    test_add_child(10, "Andrés", 9)     # Debe fallar
    
    # 3. Buscar niños
    print_section("3. BUSCAR NIÑOS POR ID")
    test_get_child(10)  # Debe encontrar a Lucas
    test_get_child(6)   # Debe encontrar a Sofía
    test_get_child(99)  # No debe encontrarlo
    
    # 4. Obtener todos los niños
    print_section("4. OBTENER TODOS LOS NIÑOS (ORDENADOS)")
    test_get_all_children()
    
    # 5. Ver estructura del árbol
    print_section("5. ESTRUCTURA DEL ÁRBOL")
    test_get_tree_structure()
    
    # 6. Recorridos
    print_section("6. RECORRIDOS DEL ÁRBOL")
    test_traversal("inorder")
    test_traversal("preorder")
    test_traversal("postorder")
    
    # 7. Estadísticas
    print_section("7. ESTADÍSTICAS DEL ÁRBOL")
    test_get_stats()
    
    # 8. Limpiar árbol
    print_section("8. LIMPIAR ÁRBOL")
    test_clear_tree()
    
    # 9. Verificar que el árbol está vacío
    print_section("9. VERIFICAR ÁRBOL VACÍO")
    test_get_stats()
    
    print_section("✓ PRUEBAS COMPLETADAS")


if __name__ == "__main__":
    main()
