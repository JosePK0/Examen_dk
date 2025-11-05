from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.ticket import Ticket, Prioridad, Estado
from domain.ports.ticket_repository import ITicketRepository
from infrastructure.database.models import TicketModel, PrioridadEnum, EstadoEnum


class TicketRepository(ITicketRepository):
    """Adaptador de repositorio para tickets (implementación con SQLAlchemy)"""
    
    def __init__(self, session: Session):
        self._session = session
    
    def _to_entity(self, model: TicketModel) -> Ticket:
        """Convierte un modelo de BD a entidad de dominio"""
        # Convertir prioridad de forma segura
        if model.prioridad:
            if isinstance(model.prioridad, PrioridadEnum):
                prioridad_value = model.prioridad.value
            elif hasattr(model.prioridad, 'value'):
                prioridad_value = model.prioridad.value
            else:
                prioridad_value = str(model.prioridad)
            prioridad_value = prioridad_value.lower()
            try:
                prioridad = Prioridad(prioridad_value)
            except ValueError:
                for p in Prioridad:
                    if p.value.lower() == prioridad_value.lower():
                        prioridad = p
                        break
                else:
                    prioridad = Prioridad.MEDIA
        else:
            prioridad = Prioridad.MEDIA
        
        # Convertir estado de forma segura
        if model.estado:
            if isinstance(model.estado, EstadoEnum):
                estado_value = model.estado.value
            elif hasattr(model.estado, 'value'):
                estado_value = model.estado.value
            else:
                estado_value = str(model.estado)
            estado_value = estado_value.lower()
            try:
                estado = Estado(estado_value)
            except ValueError:
                for e in Estado:
                    if e.value.lower() == estado_value.lower():
                        estado = e
                        break
                else:
                    estado = Estado.ABIERTO
        else:
            estado = Estado.ABIERTO
        
        return Ticket(
            ticket_id=model.ticket_id,
            usuario_id=model.usuario_id,
            tecnico_id=model.tecnico_id,
            descripcion=model.descripcion,
            prioridad=prioridad,
            estado=estado,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: Ticket) -> TicketModel:
        """Convierte una entidad de dominio a modelo de BD"""
        # Convertir prioridad de forma segura
        prioridad_value = entity.prioridad.value if hasattr(entity.prioridad, 'value') else str(entity.prioridad)
        try:
            prioridad_enum = PrioridadEnum.from_string(prioridad_value)
        except (ValueError, AttributeError):
            prioridad_enum = PrioridadEnum(prioridad_value.lower())
        
        # Convertir estado de forma segura
        estado_value = entity.estado.value if hasattr(entity.estado, 'value') else str(entity.estado)
        try:
            estado_enum = EstadoEnum.from_string(estado_value)
        except (ValueError, AttributeError):
            estado_enum = EstadoEnum(estado_value.lower())
        
        if entity.ticket_id:
            model = self._session.query(TicketModel).filter(
                TicketModel.ticket_id == entity.ticket_id
            ).first()
            if model:
                model.usuario_id = entity.usuario_id
                model.tecnico_id = entity.tecnico_id
                model.descripcion = entity.descripcion
                model.prioridad = prioridad_enum
                model.estado = estado_enum
                return model
        
        return TicketModel(
            usuario_id=entity.usuario_id,
            tecnico_id=entity.tecnico_id,
            descripcion=entity.descripcion,
            prioridad=prioridad_enum,
            estado=estado_enum
        )
    
    def crear(self, ticket: Ticket) -> Ticket:
        """Crea un nuevo ticket"""
        model = self._to_model(ticket)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def obtener_por_id(self, ticket_id: int) -> Optional[Ticket]:
        """Obtiene un ticket por su ID"""
        model = self._session.query(TicketModel).filter(
            TicketModel.ticket_id == ticket_id
        ).first()
        return self._to_entity(model) if model else None
    
    def obtener_todos(self) -> List[Ticket]:
        """Obtiene todos los tickets"""
        models = self._session.query(TicketModel).all()
        return [self._to_entity(model) for model in models]
    
    def obtener_por_usuario(self, usuario_id: int) -> List[Ticket]:
        """Obtiene todos los tickets de un usuario"""
        models = self._session.query(TicketModel).filter(
            TicketModel.usuario_id == usuario_id
        ).all()
        return [self._to_entity(model) for model in models]
    
    def obtener_por_tecnico(self, tecnico_id: int) -> List[Ticket]:
        """Obtiene todos los tickets asignados a un técnico"""
        models = self._session.query(TicketModel).filter(
            TicketModel.tecnico_id == tecnico_id
        ).all()
        return [self._to_entity(model) for model in models]
    
    def obtener_por_prioridad(self, prioridad: Prioridad) -> List[Ticket]:
        """Obtiene todos los tickets de una prioridad"""
        prioridad_value = prioridad.value if hasattr(prioridad, 'value') else str(prioridad)
        try:
            prioridad_enum = PrioridadEnum.from_string(prioridad_value)
        except (ValueError, AttributeError):
            prioridad_enum = PrioridadEnum(prioridad_value.lower())
        
        models = self._session.query(TicketModel).filter(
            TicketModel.prioridad == prioridad_enum
        ).all()
        return [self._to_entity(model) for model in models]
    
    def obtener_por_estado(self, estado: Estado) -> List[Ticket]:
        """Obtiene todos los tickets de un estado"""
        estado_value = estado.value if hasattr(estado, 'value') else str(estado)
        try:
            estado_enum = EstadoEnum.from_string(estado_value)
        except (ValueError, AttributeError):
            estado_enum = EstadoEnum(estado_value.lower())
        
        models = self._session.query(TicketModel).filter(
            TicketModel.estado == estado_enum
        ).all()
        return [self._to_entity(model) for model in models]
    
    def actualizar(self, ticket: Ticket) -> Ticket:
        """Actualiza un ticket existente"""
        model = self._session.query(TicketModel).filter(
            TicketModel.ticket_id == ticket.ticket_id
        ).first()
        
        if not model:
            raise ValueError(f"Ticket con ID {ticket.ticket_id} no encontrado")
        
        # Convertir prioridad y estado de forma segura
        prioridad_value = ticket.prioridad.value if hasattr(ticket.prioridad, 'value') else str(ticket.prioridad)
        try:
            model.prioridad = PrioridadEnum.from_string(prioridad_value)
        except (ValueError, AttributeError):
            model.prioridad = PrioridadEnum(prioridad_value.lower())
        
        estado_value = ticket.estado.value if hasattr(ticket.estado, 'value') else str(ticket.estado)
        try:
            model.estado = EstadoEnum.from_string(estado_value)
        except (ValueError, AttributeError):
            model.estado = EstadoEnum(estado_value.lower())
        
        model.usuario_id = ticket.usuario_id
        # Actualizar tecnico_id (puede ser None para desasignar)
        model.tecnico_id = ticket.tecnico_id if ticket.tecnico_id else None
        model.descripcion = ticket.descripcion
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def eliminar(self, ticket_id: int) -> bool:
        """Elimina un ticket"""
        model = self._session.query(TicketModel).filter(
            TicketModel.ticket_id == ticket_id
        ).first()
        
        if not model:
            return False
        
        self._session.delete(model)
        self._session.commit()
        return True

