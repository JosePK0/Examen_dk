from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.database.config import Base, engine
from api.routes import router
from api.usuario_routes import router as usuario_router
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear las tablas en la base de datos
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas exitosamente o ya existían")
except Exception as e:
    logger.warning(f"No se pudieron crear las tablas automáticamente: {e}")
    logger.info("Asegúrate de que la base de datos existe y ejecuta database_init.sql manualmente")

# Crear la aplicación FastAPI
app = FastAPI(
    title="HelpDeskPro API",
    description="Sistema de gestión de incidencias con arquitectura hexagonal",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(router)
app.include_router(usuario_router)
logger.info("Rutas registradas: tickets y usuarios")


@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a HelpDeskPro API",
        "version": "1.0.0",
        "docs": "/docs",
        "apis": "/apis"
    }


@app.get("/apis")
def listar_apis():
    """Lista todas las APIs disponibles"""
    return {
        "endpoints": [
            {
                "metodo": "GET",
                "ruta": "/",
                "descripcion": "Página principal de la API"
            },
            {
                "metodo": "GET",
                "ruta": "/health",
                "descripcion": "Verificar estado de la API"
            },
            {
                "metodo": "GET",
                "ruta": "/apis",
                "descripcion": "Listar todas las APIs disponibles"
            },
            {
                "metodo": "POST",
                "ruta": "/api/tickets/",
                "descripcion": "Crear un nuevo ticket",
                "body": {
                    "usuario_id": "int",
                    "descripcion": "string",
                    "prioridad": "baja|media|alta|critica"
                }
            },
            {
                "metodo": "GET",
                "ruta": "/api/tickets/",
                "descripcion": "Listar todos los tickets"
            },
            {
                "metodo": "GET",
                "ruta": "/api/tickets/{ticket_id}",
                "descripcion": "Obtener un ticket por su ID"
            },
            {
                "metodo": "PUT",
                "ruta": "/api/tickets/{ticket_id}",
                "descripcion": "Actualizar un ticket",
                "body": {
                    "descripcion": "string (opcional)",
                    "prioridad": "baja|media|alta|critica (opcional)",
                    "estado": "abierto|en_proceso|cerrado (opcional)"
                }
            },
            {
                "metodo": "POST",
                "ruta": "/api/tickets/{ticket_id}/asignar-tecnico",
                "descripcion": "Asignar un técnico a un ticket",
                "body": {
                    "tecnico_id": "int"
                }
            },
            {
                "metodo": "GET",
                "ruta": "/api/tickets/reporte/prioridad/{prioridad}",
                "descripcion": "Generar reporte de tickets por prioridad",
                "parametros": {
                    "prioridad": "baja|media|alta|critica"
                }
            },
            {
                "metodo": "GET",
                "ruta": "/api/tickets/reporte/estado/{estado}",
                "descripcion": "Generar reporte de tickets por estado",
                "parametros": {
                    "estado": "abierto|en_proceso|cerrado"
                }
            },
            {
                "metodo": "DELETE",
                "ruta": "/api/tickets/{ticket_id}",
                "descripcion": "Eliminar un ticket por su ID"
            }
        ],
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)

