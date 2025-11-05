from typing import List, Optional
from domain.entities.ticket import Ticket, Prioridad, Estado
from domain.ports.ticket_repository import ITicketRepository
from domain.ports.usuario_repository import IUsuarioRepository


class CrearTicketUseCase:
    """Caso de uso para crear un ticket"""
    
    def __init__(self, ticket_repo: ITicketRepository, usuario_repo: IUsuarioRepository):
        self._ticket_repo = ticket_repo
        self._usuario_repo = usuario_repo
    
    def ejecutar(
        self,
        usuario_id: int,
        descripcion: str,
        prioridad: Prioridad = Prioridad.MEDIA
    ) -> Ticket:
        """Ejecuta la creación de un ticket"""
        # Validar que el usuario existe
        usuario = self._usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"Usuario con ID {usuario_id} no existe")
        
        if not usuario.activo:
            raise ValueError("El usuario no está activo")
        
        # Validar descripción
        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía")
        
        # Crear ticket
        ticket = Ticket(
            usuario_id=usuario_id,
            descripcion=descripcion.strip(),
            prioridad=prioridad
        )
        
        return self._ticket_repo.crear(ticket)


class ObtenerTicketUseCase:
    """Caso de uso para obtener un ticket por ID"""
    
    def __init__(self, ticket_repo: ITicketRepository):
        self._ticket_repo = ticket_repo
    
    def ejecutar(self, ticket_id: int) -> Optional[Ticket]:
        """Ejecuta la obtención de un ticket"""
        return self._ticket_repo.obtener_por_id(ticket_id)


class ListarTicketsUseCase:
    """Caso de uso para listar tickets"""
    
    def __init__(self, ticket_repo: ITicketRepository):
        self._ticket_repo = ticket_repo
    
    def ejecutar(self) -> List[Ticket]:
        """Ejecuta la listación de todos los tickets"""
        return self._ticket_repo.obtener_todos()


class AsignarTecnicoUseCase:
    """Caso de uso para asignar un técnico a un ticket"""
    
    def __init__(self, ticket_repo: ITicketRepository, usuario_repo: IUsuarioRepository):
        self._ticket_repo = ticket_repo
        self._usuario_repo = usuario_repo
    
    def ejecutar(self, ticket_id: int, tecnico_id: int) -> Ticket:
        """Ejecuta la asignación de un técnico"""
        ticket = self._ticket_repo.obtener_por_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket con ID {ticket_id} no existe")
        
        tecnico = self._usuario_repo.obtener_por_id(tecnico_id)
        if not tecnico:
            raise ValueError(f"Técnico con ID {tecnico_id} no existe")
        
        if not tecnico.es_tecnico():
            raise ValueError(f"El usuario con ID {tecnico_id} no es un técnico")
        
        if not tecnico.activo:
            raise ValueError("El técnico no está activo")
        
        ticket.asignar_tecnico(tecnico_id)
        return self._ticket_repo.actualizar(ticket)


class ActualizarEstadoTicketUseCase:
    """Caso de uso para actualizar el estado de un ticket"""
    
    def __init__(self, ticket_repo: ITicketRepository):
        self._ticket_repo = ticket_repo
    
    def ejecutar(self, ticket_id: int, nuevo_estado: Estado) -> Ticket:
        """Ejecuta la actualización del estado"""
        ticket = self._ticket_repo.obtener_por_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket con ID {ticket_id} no existe")
        
        ticket.actualizar_estado(nuevo_estado)
        return self._ticket_repo.actualizar(ticket)


class ActualizarPrioridadTicketUseCase:
    """Caso de uso para actualizar la prioridad de un ticket"""
    
    def __init__(self, ticket_repo: ITicketRepository):
        self._ticket_repo = ticket_repo
    
    def ejecutar(self, ticket_id: int, nueva_prioridad: Prioridad) -> Ticket:
        """Ejecuta la actualización de la prioridad"""
        ticket = self._ticket_repo.obtener_por_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket con ID {ticket_id} no existe")
        
        ticket.actualizar_prioridad(nueva_prioridad)
        return self._ticket_repo.actualizar(ticket)


class GenerarReportePorPrioridadUseCase:
    """Caso de uso para generar reporte por prioridad"""
    
    def __init__(self, ticket_repo: ITicketRepository):
        self._ticket_repo = ticket_repo
    
    def ejecutar(self, prioridad: Prioridad) -> List[Ticket]:
        """Ejecuta la generación del reporte"""
        return self._ticket_repo.obtener_por_prioridad(prioridad)


class GenerarReportePorEstadoUseCase:
    """Caso de uso para generar reporte por estado"""
    
    def __init__(self, ticket_repo: ITicketRepository):
        self._ticket_repo = ticket_repo
    
    def ejecutar(self, estado: Estado) -> List[Ticket]:
        """Ejecuta la generación del reporte"""
        return self._ticket_repo.obtener_por_estado(estado)


class EliminarTicketUseCase:
    """Caso de uso para eliminar un ticket"""
    
    def __init__(self, ticket_repo: ITicketRepository):
        self._ticket_repo = ticket_repo
    
    def ejecutar(self, ticket_id: int) -> bool:
        """Ejecuta la eliminación de un ticket"""
        ticket = self._ticket_repo.obtener_por_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket con ID {ticket_id} no existe")
        
        return self._ticket_repo.eliminar(ticket_id)

