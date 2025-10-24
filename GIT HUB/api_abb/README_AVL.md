# API de Árbol AVL (Adelson-Velsky and Landis) - Children

API RESTful que implementa un Árbol AVL auto-balanceado para gestionar información de niños con ID, nombre y edad.

## 📋 Descripción

Un **Árbol AVL** es un árbol binario de búsqueda auto-balanceado que mantiene su altura balanceada mediante rotaciones automáticas. Esto garantiza que todas las operaciones (búsqueda, inserción, eliminación) se realicen en tiempo **O(log n)**.

### Características del AVL:
- ✅ Auto-balanceo mediante rotaciones (simple y doble)
- ✅ Factor de balance entre -1 y 1 para cada nodo
- ✅ Rendimiento O(log n) **garantizado** (no O(n) en el peor caso)
- ✅ Ideal para aplicaciones que requieren búsquedas frecuentes

Esta API permite:
- ✅ Agregar niños al árbol (con auto-balanceo automático)
- 🔍 Buscar niños por ID de forma eficiente
- 📊 Visualizar la estructura del árbol balanceado
- 🔄 Realizar diferentes recorridos (inorden, preorden, postorden)
- 📈 Obtener estadísticas incluyendo altura y estado de balance
- ⚖️ Verificar el balance del árbol
- 🧹 Limpiar el árbol completo

## 🚀 Instalación y Ejecución

### 1. El servidor ya está corriendo
La API incluye tanto ABB como AVL:
```
✓ Servidor activo en: http://127.0.0.1:8000
```

### 2. Acceder a la documentación
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 📚 Endpoints Disponibles

### Base URL: `/avl`

### 🏠 Inicio
- `GET /avl/` - Información de bienvenida y características del AVL

### 👶 Gestión de Niños

#### Agregar un niño (con auto-balanceo)
```http
POST /avl/children
Content-Type: application/json

{
  "id": 50,
  "name": "Ana",
  "age": 10
}
```

**Respuesta exitosa (201):**
```json
{
  "success": true,
  "message": "Niño 'Ana' con ID 50 agregado exitosamente al árbol AVL",
  "child": {
    "id": 50,
    "name": "Ana",
    "age": 10
  },
  "balanced": true,
  "tree_height": 3
}
```

**Respuesta con ID duplicado (409):**
```json
{
  "detail": "No se puede agregar el niño. El ID 50 ya existe en el árbol"
}
```

#### Buscar un niño por ID
```http
GET /avl/children/{child_id}
```

**Ejemplo:** `GET /avl/children/50`

#### Obtener todos los niños (ordenados por ID)
```http
GET /avl/children
```

### 🌳 Visualización del Árbol

#### Obtener estructura completa del árbol AVL
```http
GET /avl/tree
```

**Respuesta (200):**
```json
{
  "root": {
    "child": {
      "id": 50,
      "name": "Ana",
      "age": 10
    },
    "left": {
      "child": {
        "id": 25,
        "name": "Luis",
        "age": 8
      },
      "left": { "..." },
      "right": { "..." }
    },
    "right": {
      "child": {
        "id": 75,
        "name": "María",
        "age": 12
      },
      "left": { "..." },
      "right": { "..." }
    }
  },
  "total_children": 10
}
```

### 🔄 Recorridos del Árbol

#### Recorrido Inorden (Izquierda - Raíz - Derecha)
```http
GET /avl/traversal/inorder
```
Devuelve los niños ordenados de menor a mayor por ID.

#### Recorrido Preorden (Raíz - Izquierda - Derecha)
```http
GET /avl/traversal/preorder
```

#### Recorrido Postorden (Izquierda - Derecha - Raíz)
```http
GET /avl/traversal/postorder
```

### 📊 Estadísticas y Balance

#### Obtener estadísticas del árbol AVL
```http
GET /avl/stats
```

**Respuesta (200):**
```json
{
  "total_children": 10,
  "is_empty": false,
  "root_child": {
    "id": 50,
    "name": "Ana",
    "age": 10
  },
  "min_id": 5,
  "max_id": 80,
  "tree_height": 4,
  "is_balanced": true
}
```

#### Verificar balance del árbol
```http
GET /avl/balance
```

**Respuesta (200):**
```json
{
  "is_balanced": true,
  "tree_height": 4,
  "total_children": 10,
  "message": "El árbol AVL está correctamente balanceado"
}
```

#### Obtener cantidad de niños
```http
GET /avl/tree/count
```

### 🧹 Limpieza

#### Eliminar todos los niños del árbol
```http
DELETE /avl/tree
```

## 💡 Ejemplo de Uso Completo

```bash
# 1. Agregar niños (el árbol se auto-balancea)
curl -X POST "http://localhost:8000/avl/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 50, "name": "Ana", "age": 10}'

curl -X POST "http://localhost:8000/avl/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 25, "name": "Luis", "age": 8}'

curl -X POST "http://localhost:8000/avl/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 75, "name": "María", "age": 12}'

curl -X POST "http://localhost:8000/avl/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "name": "Carlos", "age": 6}'

# 2. Verificar que el árbol está balanceado
curl "http://localhost:8000/avl/balance"

# 3. Ver la estructura del árbol
curl "http://localhost:8000/avl/tree"

# 4. Buscar un niño específico
curl "http://localhost:8000/avl/children/50"

# 5. Obtener todos los niños ordenados
curl "http://localhost:8000/avl/children"

# 6. Ver estadísticas (incluye altura)
curl "http://localhost:8000/avl/stats"
```

## 🔑 Conceptos Clave del Árbol AVL

### ¿Qué es un Árbol AVL?
Un AVL es un ABB **auto-balanceado** inventado por Adelson-Velsky y Landis en 1962. Mantiene la propiedad de que para cada nodo, la diferencia de alturas entre sus subárboles izquierdo y derecho es como máximo 1.

### Factor de Balance
```
Factor de Balance = Altura(Subárbol Izquierdo) - Altura(Subárbol Derecho)
```

Un nodo está balanceado si su factor de balance es **-1, 0 o 1**.

### Rotaciones

El AVL usa **4 tipos de rotaciones** para mantener el balance:

#### 1. Rotación Simple Derecha (LL)
Se usa cuando el desbalance está en la izquierda del hijo izquierdo.
```
      z                y
     / \              / \
    y   C    -->     x   z
   / \                  / \
  x   B                B   C
```

#### 2. Rotación Simple Izquierda (RR)
Se usa cuando el desbalance está en la derecha del hijo derecho.
```
    z                  y
   / \                / \
  A   y      -->     z   x
     / \            / \
    B   x          A   B
```

#### 3. Rotación Doble Izquierda-Derecha (LR)
Se usa cuando el desbalance está en la derecha del hijo izquierdo.
```
      z              z              y
     / \            / \            / \
    x   D   -->    y   D   -->   x   z
     \            /                  / \
      y          x                  B   D
     /            \
    B              B
```

#### 4. Rotación Doble Derecha-Izquierda (RL)
Se usa cuando el desbalance está en la izquierda del hijo derecho.

### Ventajas del AVL

| Característica | ABB Normal | Árbol AVL |
|----------------|------------|-----------|
| Búsqueda (promedio) | O(log n) | O(log n) |
| Búsqueda (peor caso) | O(n) | **O(log n)** ✓ |
| Inserción | O(log n) - O(n) | **O(log n)** ✓ |
| Balance | ❌ No garantizado | ✅ Siempre balanceado |
| Rotaciones | ❌ No | ✅ Automáticas |

### Desventajas
- ⚠️ Más complejo de implementar (rotaciones)
- ⚠️ Overhead adicional por balanceo
- ⚠️ Más lento en inserción que un ABB simple

### Cuándo Usar AVL
- ✅ Búsquedas frecuentes
- ✅ Necesitas garantía de O(log n)
- ✅ Los datos se insertan de forma ordenada
- ✅ No puedes permitir degradación a O(n)

## 🏗️ Estructura del Proyecto

```
api_abb/
├── app/
│   ├── controllers/
│   │   ├── abb_controller.py    # Endpoints ABB
│   │   └── avl_controller.py    # Endpoints AVL ⭐
│   ├── models/
│   │   ├── abb_model.py          # Clases ABB
│   │   ├── avl_model.py          # Clases AVL con rotaciones ⭐
│   │   └── schemas.py            # Modelos Pydantic
│   ├── services/
│   │   ├── abb_service.py        # Lógica ABB
│   │   └── avl_service.py        # Lógica AVL ⭐
│   └── main.py                   # App con ABB y AVL
├── test_avl_api.py               # Pruebas AVL ⭐
├── README_ABB.md                 # Documentación ABB
└── README_AVL.md                 # Esta documentación ⭐
```

## 🧪 Pruebas

Para ejecutar las pruebas del AVL:
```bash
python test_avl_api.py
```

## 📝 Notas Técnicas

### Implementación
- ✅ Cada nodo almacena su altura
- ✅ Se actualiza la altura después de cada inserción
- ✅ Se calcula el factor de balance en cada nodo
- ✅ Se aplican rotaciones automáticamente cuando es necesario
- ✅ El árbol se mantiene balanceado en todo momento

### Complejidad Temporal

| Operación | Complejidad |
|-----------|-------------|
| Búsqueda | O(log n) ✓ |
| Inserción | O(log n) ✓ |
| Eliminación | O(log n) ✓ |
| Recorrido | O(n) |
| Obtener altura | O(1) |
| Verificar balance | O(n) |

### Complejidad Espacial
- O(n) para almacenar n nodos
- O(log n) para la pila de recursión

## 👨‍💻 Código Documentado

Todo el código está documentado línea por línea en español:

**Modelo AVL (`avl_model.py`):**
- ✅ Clase `Child`: Representa un niño
- ✅ Clase `AVLNode`: Nodo con altura
- ✅ Clase `AVLTree`: Implementación completa del AVL
  - Métodos de rotación (simple y doble)
  - Cálculo de altura y factor de balance
  - Auto-balanceo después de inserción
  - Todos los recorridos

**Servicio (`avl_service.py`):**
- ✅ `AVLService`: Lógica de negocio
- ✅ Métodos para todas las operaciones
- ✅ Verificación de balance

**Controlador (`avl_controller.py`):**
- ✅ 12 endpoints REST completos
- ✅ Documentación detallada
- ✅ Manejo de errores

## 🎯 Ejemplo Visual

### Árbol Desbalanceado vs AVL Balanceado

**Inserción secuencial en ABB (DESBALANCEADO):**
```
Insertar: 10, 20, 30, 40, 50

    10
      \
       20
         \
          30
            \
             40
               \
                50

Altura = 5 (peor caso O(n))
```

**Misma inserción en AVL (AUTO-BALANCEADO):**
```
Insertar: 10, 20, 30, 40, 50

      20
     /  \
   10    40
        /  \
       30   50

Altura = 3 (O(log n) garantizado)
```

## 🆚 Comparación: ABB vs AVL

| Aspecto | ABB | AVL |
|---------|-----|-----|
| Balanceo | Manual/No garantizado | Automático ✓ |
| Rendimiento peor caso | O(n) | O(log n) ✓ |
| Complejidad | Simple | Moderada |
| Rotaciones | No | Sí (4 tipos) |
| Altura | Puede ser n | Siempre O(log n) ✓ |
| Uso recomendado | Pocos datos, inserciones aleatorias | Muchas búsquedas, datos ordenados |

## 🌐 URLs Importantes

- API Base: http://localhost:8000
- AVL Base: http://localhost:8000/avl
- ABB Base: http://localhost:8000/abb
- Documentación: http://localhost:8000/docs

## 🎓 Referencias

- Paper original: Adelson-Velsky y Landis (1962)
- Complejidad garantizada: O(log n) para búsqueda, inserción y eliminación
- Factor de balance: Siempre entre -1 y 1

---

**¡La API del AVL está lista para usar! 🚀**

El árbol se auto-balancea automáticamente para garantizar rendimiento óptimo.
