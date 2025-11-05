from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.usuario import Usuario
from domain.ports.usuario_repository import IUsuarioRepository
from infrastructure.database.models import UsuarioModel, RolEnum


class UsuarioRepository(IUsuarioRepository):
    """Adaptador de repositorio para usuarios (implementación con SQLAlchemy)"""
    
    def __init__(self, session: Session):
        self._session = session
    
    def _to_entity(self, model: UsuarioModel) -> Usuario:
        """Convierte un modelo de BD a entidad de dominio"""
        from domain.entities.ticket import Rol
        
        # Convertir el rol de forma segura
        if model.rol:
            # Si es un enum, obtener su valor; si es string, usarlo directamente
            if isinstance(model.rol, RolEnum):
                rol_value = model.rol.value
            elif hasattr(model.rol, 'value'):
                rol_value = model.rol.value
            else:
                rol_value = str(model.rol)
            
            # Asegurar que el valor esté en minúsculas
            rol_value = rol_value.lower()
            try:
                rol = Rol(rol_value)
            except ValueError:
                # Si el valor no coincide exactamente, intentar con los valores del enum
                for r in Rol:
                    if r.value.lower() == rol_value.lower():
                        rol = r
                        break
                else:
                    rol = Rol.USUARIO  # Default
        else:
            rol = Rol.USUARIO
        
        return Usuario(
            usuario_id=model.usuario_id,
            nombre=model.nombre,
            correo=model.correo,
            contrasena=model.contrasena,
            rol=rol,
            activo=model.activo,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: Usuario) -> UsuarioModel:
        """Convierte una entidad de dominio a modelo de BD"""
        # Convertir el rol de forma segura usando el método from_string
        rol_value = entity.rol.value if hasattr(entity.rol, 'value') else str(entity.rol)
        try:
            rol_enum = RolEnum.from_string(rol_value)
        except (ValueError, AttributeError):
            # Fallback: intentar directamente
            rol_enum = RolEnum(rol_value.lower())
        
        if entity.usuario_id:
            model = self._session.query(UsuarioModel).filter(
                UsuarioModel.usuario_id == entity.usuario_id
            ).first()
            if model:
                model.nombre = entity.nombre
                model.correo = entity.correo
                model.contrasena = entity.contrasena
                model.rol = rol_enum
                model.activo = entity.activo
                return model
        
        return UsuarioModel(
            nombre=entity.nombre,
            correo=entity.correo,
            contrasena=entity.contrasena,
            rol=rol_enum,
            activo=entity.activo
        )
    
    def crear(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario"""
        model = self._to_model(usuario)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        model = self._session.query(UsuarioModel).filter(
            UsuarioModel.usuario_id == usuario_id
        ).first()
        return self._to_entity(model) if model else None
    
    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        """Obtiene un usuario por su correo"""
        model = self._session.query(UsuarioModel).filter(
            UsuarioModel.correo == correo
        ).first()
        return self._to_entity(model) if model else None
    
    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        models = self._session.query(UsuarioModel).all()
        return [self._to_entity(model) for model in models]
    
    def obtener_tecnicos(self) -> List[Usuario]:
        """Obtiene todos los técnicos"""
        models = self._session.query(UsuarioModel).filter(
            UsuarioModel.rol.in_([RolEnum.TECNICO, RolEnum.ADMIN])
        ).all()
        return [self._to_entity(model) for model in models]
    
    def actualizar(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente"""
        model = self._session.query(UsuarioModel).filter(
            UsuarioModel.usuario_id == usuario.usuario_id
        ).first()
        
        if not model:
            raise ValueError(f"Usuario con ID {usuario.usuario_id} no encontrado")
        
        # Convertir el rol de forma segura
        rol_value = usuario.rol.value if hasattr(usuario.rol, 'value') else str(usuario.rol)
        try:
            model.rol = RolEnum.from_string(rol_value)
        except (ValueError, AttributeError):
            model.rol = RolEnum(rol_value.lower())
        
        model.nombre = usuario.nombre
        model.correo = usuario.correo
        model.contrasena = usuario.contrasena
        model.activo = usuario.activo
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def eliminar(self, usuario_id: int) -> bool:
        """Elimina un usuario"""
        model = self._session.query(UsuarioModel).filter(
            UsuarioModel.usuario_id == usuario_id
        ).first()
        
        if not model:
            return False
        
        self._session.delete(model)
        self._session.commit()
        return True

