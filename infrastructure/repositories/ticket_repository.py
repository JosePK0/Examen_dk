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
        return Ticket(
            ticket_id=model.ticket_id,
            usuario_id=model.usuario_id,
            tecnico_id=model.tecnico_id,
            descripcion=model.descripcion,
            prioridad=Prioridad(model.prioridad.value),
            estado=Estado(model.estado.value),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: Ticket) -> TicketModel:
        """Convierte una entidad de dominio a modelo de BD"""
        if entity.ticket_id:
            model = self._session.query(TicketModel).filter(
                TicketModel.ticket_id == entity.ticket_id
            ).first()
            if model:
                model.usuario_id = entity.usuario_id
                model.tecnico_id = entity.tecnico_id
                model.descripcion = entity.descripcion
                model.prioridad = PrioridadEnum(entity.prioridad.value)
                model.estado = EstadoEnum(entity.estado.value)
                return model
        
        return TicketModel(
            usuario_id=entity.usuario_id,
            tecnico_id=entity.tecnico_id,
            descripcion=entity.descripcion,
            prioridad=PrioridadEnum(entity.prioridad.value),
            estado=EstadoEnum(entity.estado.value)
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
        models = self._session.query(TicketModel).filter(
            TicketModel.prioridad == PrioridadEnum(prioridad.value)
        ).all()
        return [self._to_entity(model) for model in models]
    
    def obtener_por_estado(self, estado: Estado) -> List[Ticket]:
        """Obtiene todos los tickets de un estado"""
        models = self._session.query(TicketModel).filter(
            TicketModel.estado == EstadoEnum(estado.value)
        ).all()
        return [self._to_entity(model) for model in models]
    
    def actualizar(self, ticket: Ticket) -> Ticket:
        """Actualiza un ticket existente"""
        model = self._session.query(TicketModel).filter(
            TicketModel.ticket_id == ticket.ticket_id
        ).first()
        
        if not model:
            raise ValueError(f"Ticket con ID {ticket.ticket_id} no encontrado")
        
        model.usuario_id = ticket.usuario_id
        model.tecnico_id = ticket.tecnico_id
        model.descripcion = ticket.descripcion
        model.prioridad = PrioridadEnum(ticket.prioridad.value)
        model.estado = EstadoEnum(ticket.estado.value)
        
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

