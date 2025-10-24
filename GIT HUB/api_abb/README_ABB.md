# API de Árbol Binario de Búsqueda (ABB) - Children

API RESTful que implementa un Árbol Binario de Búsqueda para gestionar información de niños con ID, nombre y edad.

## 📋 Descripción

Esta API permite:
- ✅ Agregar niños al árbol (el ID se usa como clave de ordenamiento)
- 🔍 Buscar niños por ID de forma eficiente
- 📊 Visualizar la estructura completa del árbol
- 🔄 Realizar diferentes recorridos (inorden, preorden, postorden)
- 📈 Obtener estadísticas del árbol
- 🧹 Limpiar el árbol completo

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Acceder a la documentación
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📚 Endpoints Disponibles

### Base URL: `/abb`

### 🏠 Inicio
- `GET /abb/` - Información de bienvenida y lista de endpoints

### 👶 Gestión de Niños

#### Agregar un niño
```http
POST /abb/children
Content-Type: application/json

{
  "id": 10,
  "name": "Lucas",
  "age": 7
}
```

**Respuesta exitosa (201):**
```json
{
  "success": true,
  "message": "Niño 'Lucas' con ID 10 agregado exitosamente al árbol",
  "child": {
    "id": 10,
    "name": "Lucas",
    "age": 7
  }
}
```

**Respuesta con ID duplicado (409):**
```json
{
  "detail": "No se puede agregar el niño. El ID 10 ya existe en el árbol"
}
```

#### Buscar un niño por ID
```http
GET /abb/children/{child_id}
```

**Ejemplo:** `GET /abb/children/10`

**Respuesta (200):**
```json
{
  "id": 10,
  "name": "Lucas",
  "age": 7
}
```

#### Obtener todos los niños (ordenados por ID)
```http
GET /abb/children
```

**Respuesta (200):**
```json
[
  {
    "id": 4,
    "name": "Valentina",
    "age": 6
  },
  {
    "id": 6,
    "name": "Sofía",
    "age": 5
  },
  {
    "id": 10,
    "name": "Lucas",
    "age": 7
  },
  {
    "id": 15,
    "name": "Mateo",
    "age": 8
  }
]
```

### 🌳 Visualización del Árbol

#### Obtener estructura completa del árbol
```http
GET /abb/tree
```

**Respuesta (200):**
```json
{
  "root": {
    "child": {
      "id": 10,
      "name": "Lucas",
      "age": 7
    },
    "left": {
      "child": {
        "id": 6,
        "name": "Sofía",
        "age": 5
      },
      "left": {
        "child": {
          "id": 4,
          "name": "Valentina",
          "age": 6
        },
        "left": null,
        "right": null
      },
      "right": null
    },
    "right": {
      "child": {
        "id": 15,
        "name": "Mateo",
        "age": 8
      },
      "left": null,
      "right": null
    }
  },
  "total_children": 4
}
```

### 🔄 Recorridos del Árbol

#### Recorrido Inorden (Izquierda - Raíz - Derecha)
Devuelve los niños ordenados de menor a mayor por ID.

```http
GET /abb/traversal/inorder
```

**Respuesta (200):**
```json
{
  "traversal_type": "inorden (izquierda - raíz - derecha)",
  "children": [
    {"id": 4, "name": "Valentina", "age": 6},
    {"id": 6, "name": "Sofía", "age": 5},
    {"id": 10, "name": "Lucas", "age": 7},
    {"id": 15, "name": "Mateo", "age": 8}
  ]
}
```

#### Recorrido Preorden (Raíz - Izquierda - Derecha)
```http
GET /abb/traversal/preorder
```

#### Recorrido Postorden (Izquierda - Derecha - Raíz)
```http
GET /abb/traversal/postorder
```

### 📊 Estadísticas

#### Obtener estadísticas del árbol
```http
GET /abb/stats
```

**Respuesta (200):**
```json
{
  "total_children": 4,
  "is_empty": false,
  "root_child": {
    "id": 10,
    "name": "Lucas",
    "age": 7
  },
  "min_id": 4,
  "max_id": 15
}
```

#### Obtener cantidad de niños
```http
GET /abb/tree/count
```

**Respuesta (200):**
```json
{
  "total_children": 4,
  "is_empty": false
}
```

### 🧹 Limpieza

#### Eliminar todos los niños del árbol
```http
DELETE /abb/tree
```

**Respuesta (200):**
```json
{
  "message": "Árbol limpiado exitosamente",
  "details": {
    "children_removed": 4,
    "current_count": 0
  }
}
```

## 💡 Ejemplo de Uso Completo

```bash
# 1. Agregar el primer niño (será la raíz)
curl -X POST "http://localhost:8000/abb/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "name": "Lucas", "age": 7}'

# 2. Agregar más niños
curl -X POST "http://localhost:8000/abb/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 6, "name": "Sofía", "age": 5}'

curl -X POST "http://localhost:8000/abb/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 15, "name": "Mateo", "age": 8}'

curl -X POST "http://localhost:8000/abb/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 4, "name": "Valentina", "age": 6}'

# 3. Ver la estructura del árbol
curl "http://localhost:8000/abb/tree"

# 4. Buscar un niño específico
curl "http://localhost:8000/abb/children/10"

# 5. Obtener todos los niños ordenados
curl "http://localhost:8000/abb/children"

# 6. Ver estadísticas
curl "http://localhost:8000/abb/stats"

# 7. Intentar agregar un ID duplicado (debe fallar)
curl -X POST "http://localhost:8000/abb/children" \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "name": "Andrés", "age": 9}'
```

## 🏗️ Estructura del Proyecto

```
api_abb/
├── app/
│   ├── controllers/
│   │   └── abb_controller.py    # Endpoints de la API
│   ├── models/
│   │   ├── abb_model.py          # Clases Child, Node, BinarySearchTree
│   │   └── schemas.py            # Modelos Pydantic (validación)
│   ├── services/
│   │   └── abb_service.py        # Lógica de negocio
│   └── main.py                   # Aplicación FastAPI principal
├── requirements.txt              # Dependencias
└── README_ABB.md                 # Esta documentación
```

## 🔑 Conceptos Clave del ABB

### ¿Qué es un Árbol Binario de Búsqueda?
Un ABB es una estructura de datos jerárquica donde:
- Cada nodo tiene como máximo 2 hijos (izquierdo y derecho)
- Todos los valores en el subárbol izquierdo son menores que el nodo padre
- Todos los valores en el subárbol derecho son mayores que el nodo padre
- No se permiten valores duplicados

### Ventajas
- ✅ Búsqueda eficiente: O(log n) en el caso promedio
- ✅ Inserción ordenada automática
- ✅ Recorrido inorden devuelve datos ordenados

### Reglas de Inserción
1. El primer niño agregado se convierte en la raíz
2. Si el nuevo ID < ID del nodo actual → ir a la izquierda
3. Si el nuevo ID > ID del nodo actual → ir a la derecha
4. Si el nuevo ID = ID del nodo actual → rechazar (no se permiten duplicados)

## 🧪 Pruebas

Para ejecutar las pruebas:
```bash
pytest tests/
```

## 📝 Notas Técnicas

- El árbol se mantiene en memoria (se reinicia al reiniciar el servidor)
- Los IDs deben ser números enteros positivos
- Los nombres deben tener entre 1 y 100 caracteres
- Las edades deben estar entre 0 y 150

## 👨‍💻 Código Documentado

Todo el código está documentado línea por línea en español, siguiendo las mejores prácticas de:
- ✅ Programación Orientada a Objetos (POO)
- ✅ Principios SOLID
- ✅ Separación de responsabilidades
- ✅ Encapsulamiento y abstracción
- ✅ Código limpio y mantenible

## 🎯 Ejemplo Visual del Árbol

Después de agregar los niños del ejemplo, el árbol se ve así:

```
            [10 - Lucas]
           /             \
    [6 - Sofía]       [15 - Mateo]
       /
[4 - Valentina]
```

## 🌐 URLs Importantes

- API: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health
- ABB Base: http://localhost:8000/abb

---

**¡La API está lista para usar! 🚀**
