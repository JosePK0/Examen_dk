from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from domain.entities.ticket import Prioridad, Estado, Rol


# Schemas para Ticket
class TicketCreate(BaseModel):
    """Schema para crear un ticket"""
    usuario_id: int = Field(..., description="ID del usuario que reporta el ticket")
    descripcion: str = Field(..., min_length=1, description="Descripción del problema")
    prioridad: Prioridad = Field(default=Prioridad.MEDIA, description="Prioridad del ticket")


class TicketUpdate(BaseModel):
    """Schema para actualizar un ticket"""
    descripcion: Optional[str] = Field(None, min_length=1, description="Nueva descripción")
    prioridad: Optional[Prioridad] = Field(None, description="Nueva prioridad")
    estado: Optional[Estado] = Field(None, description="Nuevo estado")


class AsignarTecnicoRequest(BaseModel):
    """Schema para asignar un técnico"""
    tecnico_id: int = Field(..., description="ID del técnico a asignar")


class TicketResponse(BaseModel):
    """Schema de respuesta para un ticket"""
    ticket_id: Optional[int]
    usuario_id: int
    tecnico_id: Optional[int]
    descripcion: str
    prioridad: Prioridad
    estado: Estado
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Schemas para Usuario
class UsuarioCreate(BaseModel):
    """Schema para crear un usuario"""
    nombre: str = Field(..., min_length=1, max_length=100)
    correo: str = Field(..., max_length=150)
    contrasena: str = Field(..., min_length=1)
    rol: Rol = Field(default=Rol.USUARIO)


class UsuarioUpdate(BaseModel):
    """Schema para actualizar un usuario"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    correo: Optional[str] = Field(None, max_length=150)
    contrasena: Optional[str] = Field(None, min_length=1)
    rol: Optional[Rol] = None


class UsuarioResponse(BaseModel):
    """Schema de respuesta para un usuario"""
    usuario_id: Optional[int]
    nombre: str
    correo: str
    rol: Rol
    activo: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

