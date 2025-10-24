---
description: Scaffold a new FastAPI project with proper structure, Pydantic models, and dependencies
---

# FastAPI Project Scaffolding

This workflow sets up a new FastAPI project with Pydantic integration and follows clean architecture principles.

## Project Structure

```
api_name/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   └── schemas.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── example_controller.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── example_service.py
│   └── utils/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── .env
```

## Prerequisites
- Python 3.8+
- pip (Python package installer)
- virtualenv (recommended)

## Usage
1. Run the workflow and provide the API name in snake_case (e.g., `my_awesome_api`)
2. The workflow will create a new directory with the provided name
3. Navigate to the project directory
4. Create and activate a virtual environment
5. Install dependencies: `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and configure your environment variables
7. Run the application: `uvicorn app.main:app --reload`

## Features
- Structured project layout following clean architecture
- Pydantic for data validation and settings management
- Environment-based configuration
- Pre-configured CORS middleware
- Basic health check endpoint
- Development and production requirements
- Git ignore file with common exclusions

### 1. Create Project Structure
```bash
# Create project directory structure
mkdir -p "${api_name}/app/{models,controllers,services,utils}"
mkdir -p "${api_name}/tests"

# Create base Python packages
touch "${api_name}/app/__init__.py"
touch "${api_name}/app/config.py"
touch "${api_name}/app/main.py"

# Create models
touch "${api_name}/app/models/__init__.py"
touch "${api_name}/app/models/base_model.py"
touch "${api_name}/app/models/schemas.py"

# Create controllers
touch "${api_name}/app/controllers/__init__.py"
touch "${api_name}/app/controllers/example_controller.py"

# Create services
touch "${api_name}/app/services/__init__.py"
touch "${api_name}/app/services/example_service.py"

# Create utils
touch "${api_name}/app/utils/__init__.py"

# Create tests
touch "${api_name}/tests/__init__.py"

# Create configuration files
touch "${api_name}/.env"
touch "${api_name}/.env.example"
touch "${api_name}/.gitignore"
touch "${api_name}/requirements.txt"
touch "${api_name}/README.md"
```

### 2. Create requirements.txt
```bash
cat > "${api_name}/requirements.txt" << 'EOL'
# Core dependencies
fastapi>=0.68.0,<0.69.0
uvicorn>=0.15.0,<0.16.0
pydantic>=1.8.0,<2.0.0
python-dotenv>=0.19.0,<0.20.0

# Development dependencies
pytest>=6.2.5,<7.0.0
pytest-cov>=2.12.1,<3.0.0
black>=21.7b0,<22.0.0
isort>=5.9.3,<6.0.0
flake8>=3.9.2,<4.0.0
mypy>=0.910,<0.920
EOL
```

### 3. Create .gitignore
```bash
cat > "${api_name}/.gitignore" << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment variables
.env

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
*.log

# Local development
.DS_Store
EOL
```

### 4. Create config.py
```bash
cat > "${api_name}/app/config.py" << 'EOL'
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "${api_name}"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Add more settings as needed
    # DATABASE_URL: str
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
EOL
```

### 5. Update main.py
```bash
cat > "${api_name}/app/main.py" << 'EOL'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI application with clean architecture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0"
    }

# Import routers here
# from app.controllers.example_controller import router as example_router
# app.include_router(example_router, prefix=f"{settings.API_V1_STR}/examples", tags=["examples"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
EOL
```

### 6. Create base_model.py
```bash
cat > "${api_name}/app/models/base_model.py" << 'EOL'
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Any

class BaseDBModel(BaseModel):
    """Base model for all database models."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ResponseModel(BaseModel):
    """Base response model for API responses."""
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[Any] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
EOL
```

### 7. Create example_controller.py
```bash
cat > "${api_name}/app/controllers/example_controller.py" << 'EOL'
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.models.base_model import ResponseModel
from app.services.example_service import ExampleService

router = APIRouter()
service = ExampleService()

@router.get("/", response_model=ResponseModel)
async def get_examples():
    """
    Get all examples.
    """
    try:
        examples = service.get_all()
        return ResponseModel(
            data=examples,
            message="Examples retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add more endpoints as needed
EOL
```

### 8. Create example_service.py
```bash
cat > "${api_name}/app/services/example_service.py" << 'EOL'
from typing import List, Optional, Dict, Any

class ExampleService:
    """
    Service layer for example operations.
    In a real application, this would interact with a database.
    """
    
    def __init__(self):
        # In a real app, this would be a database connection
        self.examples = [
            {"id": 1, "name": "Example 1"},
            {"id": 2, "name": "Example 2"}
        ]
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all examples."""
        return self.examples
    
    def get_by_id(self, example_id: int) -> Optional[Dict[str, Any]]:
        """Get an example by ID."""
        return next((e for e in self.examples if e["id"] == example_id), None)
    
    def create(self, example_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new example."""
        new_id = max(e["id"] for e in self.examples) + 1 if self.examples else 1
        example = {"id": new_id, **example_data}
        self.examples.append(example)
        return example
    
    # Add more service methods as needed
EOL
```

### 9. Create .env.example
```bash
cat > "${api_name}/.env.example" << 'EOL'
# API Settings
DEBUG=True

# Database (uncomment and configure as needed)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security (generate your own secret key)
# SECRET_KEY=your-secret-key-here
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30
EOL
```

### 10. Create README.md
```bash
cat > "${api_name}/README.md" << 'EOL'
# ${api_name}

A FastAPI-based microservice with clean architecture.

## Features

- FastAPI with Pydantic for request/response validation
- Clean architecture with separate layers (controllers, services, models)
- Environment-based configuration
- Pre-configured CORS middleware
- Health check endpoint
- Development and production requirements

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)

### Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure your environment variables:
   ```bash
   cp .env.example .env
   ```

### Running the Application

```bash
# Development (auto-reload on changes)
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI Schema: `/api/v1/openapi.json`

## Project Structure

```
.
├── app/                    # Application package
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Application configuration
│   ├── main.py             # Application entry point
│   ├── models/             # Data models and schemas
│   ├── controllers/        # Request handlers
│   ├── services/           # Business logic
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Development

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code with black and isort
black .
isort .
```

## License

[Your License Here]
EOL
```

## Project Created Successfully

Your FastAPI project has been created with the following structure:
- Clean architecture with separate layers (controllers, services, models)
- Pydantic for data validation and settings management
- Environment-based configuration
- Pre-configured CORS middleware
- Health check endpoint
- Development and production requirements
- Basic API documentation
- Example controller and service
- Git ignore file with common exclusions
