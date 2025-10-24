from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import abb_controller, avl_controller

# Crear instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Estructuras de Datos - ABB y AVL",
    description="API RESTful para gestionar Árboles Binarios de Búsqueda (ABB) y Árboles AVL de niños con ID, nombre y edad",
    version="2.0.0",
    docs_url="/docs",  # Documentación interactiva en /docs
    redoc_url="/redoc"  # Documentación alternativa en /redoc
)

# Configurar CORS para permitir peticiones desde otros orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (cambiar en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

# Registrar el router del ABB con el prefijo /abb
app.include_router(
    abb_controller.router,
    prefix="/abb",
    tags=["Árbol Binario de Búsqueda (ABB)"]
)

# Registrar el router del AVL con el prefijo /avl
app.include_router(
    avl_controller.router,
    prefix="/avl",
    tags=["Árbol AVL (Auto-balanceado)"]
)


# Endpoint raíz de bienvenida
@app.get("/")
async def root():
    """
    Endpoint raíz de la API.
    Proporciona información básica sobre la API.
    
    Returns:
        Diccionario con información de bienvenida
    """
    return {
        "message": "API de Estructuras de Datos - ABB y AVL",
        "version": "2.0.0",
        "description": "API para gestionar árboles binarios de búsqueda (ABB) y árboles AVL auto-balanceados",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "available_trees": {
            "abb": {
                "name": "Árbol Binario de Búsqueda",
                "base_path": "/abb",
                "description": "ABB estándar sin auto-balanceo",
                "info_endpoint": "/abb/"
            },
            "avl": {
                "name": "Árbol AVL",
                "base_path": "/avl",
                "description": "Árbol AVL auto-balanceado con rotaciones",
                "info_endpoint": "/avl/"
            }
        },
        "status": "online"
    }


# Endpoint de health check
@app.get("/health")
async def health_check():
    """
    Verifica el estado de salud de la API.
    
    Returns:
        Diccionario con el estado de la API
    """
    return {
        "status": "healthy",
        "service": "ABB & AVL API",
        "trees_available": ["ABB", "AVL"]
    }
