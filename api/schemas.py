from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from domain.entities.ticket import Prioridad, Estado, Rol


# Schemas para Ticket
class TicketCreate(BaseModel):
    """Schema para crear un ticket"""
    usuario_id: int = Field(..., gt=0, description="ID del usuario que reporta el ticket (debe ser mayor a 0)")
    descripcion: str = Field(..., min_length=10, max_length=2000, 
                            description="Descripción del problema (10-2000 caracteres)")
    prioridad: Prioridad = Field(default=Prioridad.MEDIA, description="Prioridad del ticket")

    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v):
        if not v or not v.strip() or len(v.strip()) < 10:
            raise ValueError('La descripción debe tener al menos 10 caracteres')
        return v.strip()


class TicketUpdate(BaseModel):
    """Schema para actualizar un ticket"""
    descripcion: Optional[str] = Field(None, min_length=10, max_length=2000,
                                      description="Nueva descripción (10-2000 caracteres)")
    prioridad: Optional[Prioridad] = Field(None, description="Nueva prioridad")
    estado: Optional[Estado] = Field(None, description="Nuevo estado")
    tecnico_id: Optional[int] = Field(None, ge=0, description="ID del técnico a asignar (0 o None para desasignar)")

    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v):
        if v is not None:
            if not v.strip() or len(v.strip()) < 10:
                raise ValueError('La descripción debe tener al menos 10 caracteres')
            return v.strip()
        return v


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
        use_enum_values = True


# Schemas para Usuario
class UsuarioCreate(BaseModel):
    """Schema para crear un usuario"""
    nombre: str = Field(..., min_length=2, max_length=100, 
                       description="Nombre del usuario (2-100 caracteres, solo letras y espacios)")
    correo: str = Field(..., max_length=150, 
                       description="Correo electrónico válido")
    contrasena: str = Field(..., min_length=6, max_length=255,
                           description="Contraseña (mínimo 6 caracteres)")
    rol: Rol = Field(default=Rol.USUARIO, description="Rol del usuario")

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v):
        import re
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', v.strip()):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.strip()

    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v):
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Ingrese un correo electrónico válido')
        return v.lower().strip()


class UsuarioUpdate(BaseModel):
    """Schema para actualizar un usuario"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100,
                                  description="Nombre del usuario (2-100 caracteres)")
    correo: Optional[str] = Field(None, max_length=150,
                                 description="Correo electrónico válido")
    contrasena: Optional[str] = Field(None, min_length=6, max_length=255,
                                      description="Contraseña (mínimo 6 caracteres)")
    rol: Optional[Rol] = Field(None, description="Rol del usuario")

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v):
        if v is not None:
            import re
            if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', v.strip()):
                raise ValueError('El nombre solo puede contener letras y espacios')
            return v.strip()
        return v

    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v):
        if v is not None:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, v):
                raise ValueError('Ingrese un correo electrónico válido')
            return v.lower().strip()
        return v


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

