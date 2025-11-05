from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.database.config import Base
import enum


class PrioridadEnum(enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class EstadoEnum(enum.Enum):
    ABIERTO = "abierto"
    EN_PROCESO = "en_proceso"
    CERRADO = "cerrado"


class RolEnum(enum.Enum):
    USUARIO = "usuario"
    TECNICO = "tecnico"
    ADMIN = "admin"
    
    @classmethod
    def from_string(cls, value: str):
        """Convierte un string a RolEnum de forma segura"""
        value_lower = value.lower()
        for role in cls:
            if role.value == value_lower:
                return role
        raise ValueError(f"'{value}' no es un rol válido. Valores válidos: {[r.value for r in cls]}")


class UsuarioModel(Base):
    """Modelo SQLAlchemy para la tabla usuarios"""
    __tablename__ = "usuarios"
    
    usuario_id = Column("IDusuario", Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum, values_callable=lambda x: [e.value for e in RolEnum]), default=RolEnum.USUARIO, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    created_at = Column("createdAt", DateTime, server_default=func.now())
    updated_at = Column("updatedAt", DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    tickets_usuario = relationship("TicketModel", foreign_keys="TicketModel.usuario_id", back_populates="usuario")
    tickets_tecnico = relationship("TicketModel", foreign_keys="TicketModel.tecnico_id", back_populates="tecnico")


class TicketModel(Base):
    """Modelo SQLAlchemy para la tabla tickets"""
    __tablename__ = "tickets"
    
    ticket_id = Column("IDticket", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuarioID", Integer, ForeignKey("usuarios.IDusuario", ondelete="CASCADE"), nullable=False)
    tecnico_id = Column("tecnicoID", Integer, ForeignKey("usuarios.IDusuario", ondelete="SET NULL"), nullable=True)
    descripcion = Column(Text, nullable=False)
    prioridad = Column(Enum(PrioridadEnum), default=PrioridadEnum.MEDIA, nullable=False)
    estado = Column(Enum(EstadoEnum), default=EstadoEnum.ABIERTO, nullable=False)
    created_at = Column("createdAt", DateTime, server_default=func.now())
    updated_at = Column("updatedAt", DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    usuario = relationship("UsuarioModel", foreign_keys=[usuario_id], back_populates="tickets_usuario")
    tecnico = relationship("UsuarioModel", foreign_keys=[tecnico_id], back_populates="tickets_tecnico")

