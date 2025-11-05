from datetime import datetime
from typing import Optional
from domain.entities.ticket import Rol


class Usuario:
    """Entidad de dominio para Usuario"""
    
    def __init__(
        self,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: Rol = Rol.USUARIO,
        activo: bool = True,
        usuario_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol
        self.activo = activo
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def es_tecnico(self) -> bool:
        """Verifica si el usuario es técnico"""
        return self.rol in [Rol.TECNICO, Rol.ADMIN]
    
    def desactivar(self) -> None:
        """Desactiva el usuario"""
        self.activo = False
        self.updated_at = datetime.now()
    
    def activar(self) -> None:
        """Activa el usuario"""
        self.activo = True
        self.updated_at = datetime.now()

