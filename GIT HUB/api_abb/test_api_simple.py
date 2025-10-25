"""
Test simple de la API usando urllib (sin dependencias externas)
"""
import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000/abb"

def test_api():
    print("=" * 70)
    print("PRUEBA DE API CON PYDANTIC")
    print("=" * 70)
    
    # Test 1: Agregar un nino valido
    print("\n[TEST 1] Agregando nino valido (ID=10, nombre=Lucas, edad=7)")
    try:
        data = json.dumps({"id": 10, "name": "Lucas", "age": 7}).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/children", data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Respuesta: {result['message']}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 2: Agregar otro nino
    print("\n[TEST 2] Agregando nino (ID=5, nombre=Sofia, edad=6)")
    try:
        data = json.dumps({"id": 5, "name": "Sofia", "age": 6}).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/children", data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Respuesta: {result['message']}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 3: Intentar agregar ID duplicado
    print("\n[TEST 3] Intentando agregar ID duplicado (ID=10)")
    try:
        data = json.dumps({"id": 10, "name": "Pedro", "age": 8}).encode('utf-8')
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
    
    # Test 4: Intentar agregar con edad negativa (validacion Pydantic)
    print("\n[TEST 4] Intentando agregar nino con edad negativa")
    try:
        data = json.dumps({"id": 20, "name": "Maria", "age": -5}).encode('utf-8')
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
    
    # Test 5: Intentar agregar con nombre vacio (validacion Pydantic)
    print("\n[TEST 5] Intentando agregar nino con nombre vacio")
    try:
        data = json.dumps({"id": 25, "name": "", "age": 10}).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/children", data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[ERROR] Se acepto nombre vacio: {result}")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"[OK] Validacion Pydantic funciono - nombre vacio rechazado (HTTP 422)")
        else:
            print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 6: Buscar un nino
    print("\n[TEST 6] Buscando nino con ID=10")
    try:
        req = urllib.request.Request(f"{BASE_URL}/children/10")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Nino encontrado: {json.dumps(result, indent=2)}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 7: Obtener todos los ninos
    print("\n[TEST 7] Obteniendo todos los ninos (recorrido inorden)")
    try:
        req = urllib.request.Request(f"{BASE_URL}/children")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Total de ninos: {len(result)}")
        print(f"Lista ordenada por ID: {json.dumps(result, indent=2)}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 8: Obtener estructura del arbol
    print("\n[TEST 8] Obteniendo estructura del arbol")
    try:
        req = urllib.request.Request(f"{BASE_URL}/tree")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Total de ninos en el arbol: {result['total_children']}")
        print(f"Estructura: {json.dumps(result, indent=2)}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 9: Recorrido inorden
    print("\n[TEST 9] Recorrido inorden")
    try:
        req = urllib.request.Request(f"{BASE_URL}/traversal/inorder")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Tipo: {result['traversal_type']}")
        print(f"Ninos: {json.dumps(result['children'], indent=2)}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    # Test 10: Estadisticas
    print("\n[TEST 10] Obteniendo estadisticas")
    try:
        req = urllib.request.Request(f"{BASE_URL}/stats")
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(f"[OK] Estadisticas: {json.dumps(result, indent=2)}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    test_api()
