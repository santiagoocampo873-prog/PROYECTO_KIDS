"""
Script de prueba para la API del Árbol AVL.
Este script demuestra todas las funcionalidades de la API AVL,
incluyendo las rotaciones automáticas para mantener el árbol balanceado.
"""

import requests
import json

# URL base de la API AVL
BASE_URL = "http://localhost:8000/avl"

# Colores para output en consola
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
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


def print_warning(message):
    """Imprime un mensaje de advertencia en magenta"""
    print(f"{Colors.MAGENTA}⚠ {message}{Colors.END}")


def print_section(title):
    """Imprime un título de sección"""
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}\n")


def test_add_child(id, name, age):
    """
    Prueba agregar un niño al árbol AVL.
    
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
            print_success(f"Niño agregado: {result['message']}")
            if 'balanced' in result:
                balance_status = "✓ BALANCEADO" if result['balanced'] else "✗ DESBALANCEADO"
                print_warning(f"Estado del árbol: {balance_status}, Altura: {result.get('tree_height', 'N/A')}")
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
    print_info("Obteniendo estructura del árbol AVL")
    
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
    print_info("Obteniendo estadísticas del árbol AVL")
    
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


def test_check_balance():
    """Prueba verificar el balance del árbol AVL"""
    print_info("Verificando balance del árbol AVL")
    
    try:
        # Hacer la petición GET
        response = requests.get(f"{BASE_URL}/balance")
        
        # Verificar el resultado
        if response.status_code == 200:
            balance = response.json()
            if balance['is_balanced']:
                print_success(f"✓ {balance['message']}")
            else:
                print_error(f"✗ {balance['message']}")
            print(json.dumps(balance, indent=2, ensure_ascii=False))
            return balance
        else:
            print_error(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None


def test_clear_tree():
    """Prueba limpiar el árbol completo"""
    print_info("Limpiando el árbol AVL completo")
    
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
    
    print_section("PRUEBA COMPLETA DE LA API DEL ÁRBOL AVL")
    
    # Verificar que la API esté activa
    print_info("Verificando conexión con la API AVL...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success("Conexión exitosa con la API AVL")
        else:
            print_error("La API no está respondiendo correctamente")
            return
    except Exception as e:
        print_error(f"No se puede conectar a la API: {e}")
        print_info("Asegúrate de que la API esté corriendo: uvicorn app.main:app --reload")
        return
    
    # 1. Agregar niños que causarán rotaciones
    print_section("1. AGREGAR NIÑOS AL ÁRBOL AVL (con auto-balanceo)")
    print_warning("El árbol AVL se auto-balancea mediante rotaciones")
    
    # Estos nodos causarán diferentes tipos de rotaciones
    test_add_child(50, "Ana", 10)      # Raíz
    test_add_child(25, "Luis", 8)      # Izquierda
    test_add_child(75, "María", 12)    # Derecha
    test_add_child(10, "Carlos", 6)    # Izquierda-Izquierda
    test_add_child(30, "Elena", 9)     # Izquierda-Derecha
    test_add_child(60, "Pedro", 11)    # Derecha-Izquierda
    test_add_child(80, "Sofía", 7)     # Derecha-Derecha
    
    # Agregar más nodos para forzar rotaciones complejas
    test_add_child(5, "Juan", 5)
    test_add_child(15, "Laura", 8)
    test_add_child(70, "Diego", 10)
    
    # 2. Verificar el balance después de las inserciones
    print_section("2. VERIFICAR BALANCE DEL ÁRBOL")
    test_check_balance()
    
    # 3. Intentar agregar ID duplicado
    print_section("3. PROBAR ID DUPLICADO")
    test_add_child(50, "Duplicado", 15)  # Debe fallar
    
    # 4. Buscar niños
    print_section("4. BUSCAR NIÑOS POR ID")
    test_get_child(50)  # Debe encontrar a Ana
    test_get_child(10)  # Debe encontrar a Carlos
    test_get_child(99)  # No debe encontrarlo
    
    # 5. Obtener todos los niños
    print_section("5. OBTENER TODOS LOS NIÑOS (ORDENADOS)")
    test_get_all_children()
    
    # 6. Ver estructura del árbol
    print_section("6. ESTRUCTURA DEL ÁRBOL AVL BALANCEADO")
    test_get_tree_structure()
    
    # 7. Recorridos
    print_section("7. RECORRIDOS DEL ÁRBOL AVL")
    test_traversal("inorder")
    test_traversal("preorder")
    test_traversal("postorder")
    
    # 8. Estadísticas (incluye altura del árbol)
    print_section("8. ESTADÍSTICAS DEL ÁRBOL AVL")
    test_get_stats()
    
    # 9. Verificar balance nuevamente
    print_section("9. VERIFICACIÓN FINAL DE BALANCE")
    test_check_balance()
    
    # 10. Limpiar árbol
    print_section("10. LIMPIAR ÁRBOL")
    test_clear_tree()
    
    # 11. Verificar que el árbol está vacío
    print_section("11. VERIFICAR ÁRBOL VACÍO")
    test_get_stats()
    
    print_section("✓ PRUEBAS AVL COMPLETADAS")
    print_warning("El árbol AVL mantiene el balance automáticamente mediante rotaciones")
    print_info("Todas las operaciones tienen complejidad O(log n) garantizada")


if __name__ == "__main__":
    main()
