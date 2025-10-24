# API ABB

API RESTful construida con FastAPI siguiendo principios de Programación Orientada a Objetos y arquitectura limpia.

## 🏗️ Estructura del Proyecto

```
api_abb/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── config.py               # Configuración con Pydantic
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py       # Modelos base reutilizables
│   │   └── schemas.py          # Schemas de Pydantic para validación
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── example_controller.py  # Endpoints REST
│   ├── services/
│   │   ├── __init__.py
│   │   └── example_service.py     # Lógica de negocio
│   └── utils/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── .env.example                # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt            # Dependencias del proyecto
└── README.md
```

## 🚀 Características

- **FastAPI**: Framework moderno y rápido para construir APIs
- **Pydantic**: Validación de datos y configuración basada en tipos
- **Arquitectura limpia**: Separación de responsabilidades (Controllers, Services, Models)
- **POO**: Implementación siguiendo principios de encapsulamiento, abstracción y herencia
- **CORS**: Middleware configurado para peticiones cross-origin
- **Documentación automática**: Swagger UI y ReDoc incluidos

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- virtualenv (recomendado)

## 🔧 Instalación

### 1. Clonar o navegar al directorio del proyecto

```bash
cd api_abb
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus configuraciones
```

## ▶️ Ejecución

### Modo desarrollo (con hot-reload)

```bash
uvicorn app.main:app --reload
```

### Modo producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación

Una vez que la aplicación esté corriendo, puedes acceder a:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🧪 Endpoints Disponibles

### Health Check
- `GET /` - Endpoint raíz
- `GET /health` - Verificación de salud de la API

### Examples (CRUD completo)
- `POST /api/v1/examples` - Crear un nuevo ejemplo
- `GET /api/v1/examples` - Obtener todos los ejemplos
- `GET /api/v1/examples/{id}` - Obtener un ejemplo específico
- `PUT /api/v1/examples/{id}` - Actualizar un ejemplo
- `DELETE /api/v1/examples/{id}` - Eliminar un ejemplo

## 💡 Ejemplo de Uso

### Crear un ejemplo

```bash
curl -X POST "http://localhost:8000/api/v1/examples" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Ejemplo",
    "description": "Descripción del ejemplo",
    "is_active": true
  }'
```

### Obtener todos los ejemplos

```bash
curl -X GET "http://localhost:8000/api/v1/examples"
```

## 🏛️ Principios de POO Implementados

### Encapsulamiento
- Los servicios encapsulan la lógica de negocio
- Los modelos encapsulan la estructura de datos y validaciones

### Abstracción
- `BaseModelWithTimestamp` proporciona funcionalidad común
- Separación clara entre schemas de entrada/salida

### Herencia
- `ExampleResponse` hereda de `ExampleBase` y `BaseModelWithTimestamp`
- Reutilización de código mediante clases base

### Polimorfismo
- Diferentes schemas para diferentes operaciones (Create, Update, Response)
- Métodos con comportamientos específicos según el contexto

### Separación de Responsabilidades (SOLID)
- **Controllers**: Manejan las peticiones HTTP
- **Services**: Contienen la lógica de negocio
- **Models**: Definen la estructura y validación de datos
- **Config**: Gestiona la configuración de la aplicación

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/
```

## 🛠️ Desarrollo

### Formateo de código

```bash
# Black para formateo
black app/

# isort para ordenar imports
isort app/

# flake8 para linting
flake8 app/
```

### Type checking

```bash
mypy app/
```

## 📝 Próximos Pasos

- [ ] Integrar base de datos (PostgreSQL, MySQL, etc.)
- [ ] Implementar autenticación y autorización (JWT)
- [ ] Agregar más endpoints según necesidades del negocio
- [ ] Implementar logging estructurado
- [ ] Agregar tests unitarios e integración
- [ ] Configurar CI/CD
- [ ] Dockerizar la aplicación

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.
