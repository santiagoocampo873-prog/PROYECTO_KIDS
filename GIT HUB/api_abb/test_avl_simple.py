"""
Test simple de la API AVL usando urllib (sin dependencias externas)
"""
import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000/avl"

def test_avl_api():
    print("=" * 70)
    print("PRUEBA DE API AVL CON PYDANTIC")
    print("=" * 70)
    
    # Test 1: Agregar ninos para probar auto-balanceo
    print("\n[TEST 1] Agregando ninos para probar auto-balanceo del AVL")
    test_data = [
        {"id": 10, "name": "Nodo10", "age": 10},
        {"id": 20, "name": "Nodo20", "age": 11},
        {"id": 30, "name": "Nodo30", "age": 12},  # Esto causara rotacion
        {"id": 5, "name": "Nodo5", "age": 8},
        {"id": 15, "name": "Nodo15", "age": 9}
    ]
    
    for child_data in test_data:
        try:
            data = json.dumps(child_data).encode('utf-8')
            req = urllib.request.Request(f"{BASE_URL}/children", data=data, headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode('utf-8'))
            print(f"[OK] Agregado: {child_data['name']} (ID={child_data['id']})")
        except urllib.error.HTTPError as e:
            print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"[ERROR] {e}")
    
    # Test 2: Verificar que el arbol esta balanceado
    print("\n[TEST 2] Verificando que el arbol AVL esta balanceado")
    try:
        req = urllib.request.Request(f"{BASE_URL}/stats")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Total de ninos: {result['total_children']}")
        print(f"[OK] Altura del arbol: {result['tree_height']}")
        print(f"[OK] Esta balanceado: {result['is_balanced']}")
        if result['is_balanced']:
            print("[OK] El arbol AVL se auto-balancea correctamente!")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 3: Intentar agregar ID duplicado
    print("\n[TEST 3] Intentando agregar ID duplicado (ID=10)")
    try:
        data = json.dumps({"id": 10, "name": "Duplicado", "age": 8}).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/children", data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[ERROR] Se acepto ID duplicado: {result}")
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print(f"[OK] Validacion correcta - ID duplicado rechazado (HTTP 409)")
        else:
            print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 4: Validacion Pydantic - edad negativa
    print("\n[TEST 4] Intentando agregar nino con edad negativa")
    try:
        data = json.dumps({"id": 100, "name": "Maria", "age": -5}).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/children", data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[ERROR] Se acepto edad negativa: {result}")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"[OK] Validacion Pydantic funciono - edad negativa rechazada (HTTP 422)")
        else:
            print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 5: Buscar un nino
    print("\n[TEST 5] Buscando nino con ID=15")
    try:
        req = urllib.request.Request(f"{BASE_URL}/children/15")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Nino encontrado: {json.dumps(result, indent=2)}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 6: Obtener estructura del arbol (ver balanceo)
    print("\n[TEST 6] Obteniendo estructura del arbol AVL (ver balanceo)")
    try:
        req = urllib.request.Request(f"{BASE_URL}/tree")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Estructura del arbol balanceado:")
        print(json.dumps(result, indent=2))
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 7: Recorrido inorden (debe estar ordenado)
    print("\n[TEST 7] Recorrido inorden (debe estar ordenado por ID)")
    try:
        req = urllib.request.Request(f"{BASE_URL}/traversal/inorder")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Tipo: {result['traversal_type']}")
        print(f"Ninos ordenados: {json.dumps(result['children'], indent=2)}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 8: Verificar altura del arbol AVL
    print("\n[TEST 8] Verificando altura del arbol AVL")
    print("Con 5 nodos, un arbol balanceado debe tener altura maxima de 3")
    try:
        req = urllib.request.Request(f"{BASE_URL}/stats")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        altura = result['tree_height']
        print(f"[OK] Altura actual: {altura}")
        if altura <= 3:
            print("[OK] La altura es optima para un AVL con 5 nodos!")
        else:
            print("[WARNING] La altura es mayor de lo esperado")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n" + "=" * 70)
    print("PRUEBAS AVL COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    test_avl_api()
