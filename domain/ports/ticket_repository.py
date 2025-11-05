from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.ticket import Ticket, Prioridad, Estado


class ITicketRepository(ABC):
    """Puerto (interfaz) para el repositorio de tickets"""
    
    @abstractmethod
    def crear(self, ticket: Ticket) -> Ticket:
        """Crea un nuevo ticket"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, ticket_id: int) -> Optional[Ticket]:
        """Obtiene un ticket por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Ticket]:
        """Obtiene todos los tickets"""
        pass
    
    @abstractmethod
    def obtener_por_usuario(self, usuario_id: int) -> List[Ticket]:
        """Obtiene todos los tickets de un usuario"""
        pass
    
    @abstractmethod
    def obtener_por_tecnico(self, tecnico_id: int) -> List[Ticket]:
        """Obtiene todos los tickets asignados a un técnico"""
        pass
    
    @abstractmethod
    def obtener_por_prioridad(self, prioridad: Prioridad) -> List[Ticket]:
        """Obtiene todos los tickets de una prioridad"""
        pass
    
    @abstractmethod
    def obtener_por_estado(self, estado: Estado) -> List[Ticket]:
        """Obtiene todos los tickets de un estado"""
        pass
    
    @abstractmethod
    def actualizar(self, ticket: Ticket) -> Ticket:
        """Actualiza un ticket existente"""
        pass
    
    @abstractmethod
    def eliminar(self, ticket_id: int) -> bool:
        """Elimina un ticket"""
        pass

