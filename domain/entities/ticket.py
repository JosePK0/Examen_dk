from datetime import datetime
from typing import Optional
from enum import Enum


class Prioridad(str, Enum):
    """Enum para las prioridades de tickets"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class Estado(str, Enum):
    """Enum para los estados de tickets"""
    ABIERTO = "abierto"
    EN_PROCESO = "en_proceso"
    CERRADO = "cerrado"


class Rol(str, Enum):
    """Enum para los roles de usuario"""
    USUARIO = "usuario"
    TECNICO = "tecnico"
    ADMIN = "admin"


class Ticket:
    """Entidad de dominio para Ticket"""
    
    def __init__(
        self,
        usuario_id: int,
        descripcion: str,
        prioridad: Prioridad = Prioridad.MEDIA,
        estado: Estado = Estado.ABIERTO,
        tecnico_id: Optional[int] = None,
        ticket_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.ticket_id = ticket_id
        self.usuario_id = usuario_id
        self.tecnico_id = tecnico_id
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = estado
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def asignar_tecnico(self, tecnico_id: int) -> None:
        """Asigna un técnico al ticket"""
        if self.estado == Estado.CERRADO:
            raise ValueError("No se puede asignar un técnico a un ticket cerrado")
        self.tecnico_id = tecnico_id
        if self.estado == Estado.ABIERTO:
            self.estado = Estado.EN_PROCESO
        self.updated_at = datetime.now()
    
    def actualizar_estado(self, nuevo_estado: Estado) -> None:
        """Actualiza el estado del ticket"""
        if nuevo_estado == Estado.CERRADO and self.estado == Estado.ABIERTO:
            raise ValueError("No se puede cerrar un ticket sin estar en proceso")
        self.estado = nuevo_estado
        self.updated_at = datetime.now()
    
    def actualizar_prioridad(self, nueva_prioridad: Prioridad) -> None:
        """Actualiza la prioridad del ticket"""
        self.prioridad = nueva_prioridad
        self.updated_at = datetime.now()
    
    def actualizar_descripcion(self, nueva_descripcion: str) -> None:
        """Actualiza la descripción del ticket"""
        if not nueva_descripcion.strip():
            raise ValueError("La descripción no puede estar vacía")
        self.descripcion = nueva_descripcion
        self.updated_at = datetime.now()

