from fastapi import Depends
from sqlalchemy.orm import Session
from infrastructure.database.config import get_db_session
from infrastructure.repositories.ticket_repository import TicketRepository
from infrastructure.repositories.usuario_repository import UsuarioRepository
from domain.ports.ticket_repository import ITicketRepository
from domain.ports.usuario_repository import IUsuarioRepository
from domain.use_cases.ticket_use_cases import (
    CrearTicketUseCase,
    ObtenerTicketUseCase,
    ListarTicketsUseCase,
    AsignarTecnicoUseCase,
    ActualizarEstadoTicketUseCase,
    ActualizarPrioridadTicketUseCase,
    GenerarReportePorPrioridadUseCase,
    GenerarReportePorEstadoUseCase,
    EliminarTicketUseCase
)


def get_ticket_repository(db: Session = Depends(get_db_session)) -> ITicketRepository:
    """Dependency Injection: Provee el repositorio de tickets"""
    return TicketRepository(db)


def get_usuario_repository(db: Session = Depends(get_db_session)) -> IUsuarioRepository:
    """Dependency Injection: Provee el repositorio de usuarios"""
    return UsuarioRepository(db)


def get_crear_ticket_use_case(
    ticket_repo: ITicketRepository,
    usuario_repo: IUsuarioRepository
) -> CrearTicketUseCase:
    """Dependency Injection: Provee el caso de uso de crear ticket"""
    return CrearTicketUseCase(ticket_repo, usuario_repo)


def get_obtener_ticket_use_case(
    ticket_repo: ITicketRepository
) -> ObtenerTicketUseCase:
    """Dependency Injection: Provee el caso de uso de obtener ticket"""
    return ObtenerTicketUseCase(ticket_repo)


def get_listar_tickets_use_case(
    ticket_repo: ITicketRepository
) -> ListarTicketsUseCase:
    """Dependency Injection: Provee el caso de uso de listar tickets"""
    return ListarTicketsUseCase(ticket_repo)


def get_asignar_tecnico_use_case(
    ticket_repo: ITicketRepository,
    usuario_repo: IUsuarioRepository
) -> AsignarTecnicoUseCase:
    """Dependency Injection: Provee el caso de uso de asignar técnico"""
    return AsignarTecnicoUseCase(ticket_repo, usuario_repo)


def get_actualizar_estado_use_case(
    ticket_repo: ITicketRepository
) -> ActualizarEstadoTicketUseCase:
    """Dependency Injection: Provee el caso de uso de actualizar estado"""
    return ActualizarEstadoTicketUseCase(ticket_repo)


def get_actualizar_prioridad_use_case(
    ticket_repo: ITicketRepository
) -> ActualizarPrioridadTicketUseCase:
    """Dependency Injection: Provee el caso de uso de actualizar prioridad"""
    return ActualizarPrioridadTicketUseCase(ticket_repo)


def get_reporte_prioridad_use_case(
    ticket_repo: ITicketRepository
) -> GenerarReportePorPrioridadUseCase:
    """Dependency Injection: Provee el caso de uso de reporte por prioridad"""
    return GenerarReportePorPrioridadUseCase(ticket_repo)


def get_reporte_estado_use_case(
    ticket_repo: ITicketRepository
) -> GenerarReportePorEstadoUseCase:
    """Dependency Injection: Provee el caso de uso de reporte por estado"""
    return GenerarReportePorEstadoUseCase(ticket_repo)


def get_eliminar_ticket_use_case(
    ticket_repo: ITicketRepository
) -> EliminarTicketUseCase:
    """Dependency Injection: Provee el caso de uso de eliminar ticket"""
    return EliminarTicketUseCase(ticket_repo)

