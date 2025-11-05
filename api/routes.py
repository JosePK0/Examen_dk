from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from domain.entities.ticket import Prioridad, Estado
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
from domain.ports.ticket_repository import ITicketRepository
from domain.ports.usuario_repository import IUsuarioRepository
from api.schemas import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    AsignarTecnicoRequest
)
from api.dependencies import (
    get_ticket_repository,
    get_usuario_repository
)

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def crear_ticket(
    ticket_data: TicketCreate,
    ticket_repo: ITicketRepository = Depends(get_ticket_repository),
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
):
    """
    Crea un nuevo ticket.
    
    - **usuario_id**: ID del usuario que reporta el ticket
    - **descripcion**: Descripción del problema
    - **prioridad**: Prioridad del ticket (baja, media, alta, critica)
    """
    try:
        use_case = CrearTicketUseCase(ticket_repo, usuario_repo)
        ticket = use_case.ejecutar(
            usuario_id=ticket_data.usuario_id,
            descripcion=ticket_data.descripcion,
            prioridad=ticket_data.prioridad
        )
        
        return TicketResponse(
            ticket_id=ticket.ticket_id,
            usuario_id=ticket.usuario_id,
            tecnico_id=ticket.tecnico_id,
            descripcion=ticket.descripcion,
            prioridad=ticket.prioridad,
            estado=ticket.estado,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[TicketResponse])
def listar_tickets(
    ticket_repo: ITicketRepository = Depends(get_ticket_repository)
):
    """
    Lista todos los tickets.
    """
    use_case = ListarTicketsUseCase(ticket_repo)
    tickets = use_case.ejecutar()
    
    return [
        TicketResponse(
            ticket_id=t.ticket_id,
            usuario_id=t.usuario_id,
            tecnico_id=t.tecnico_id,
            descripcion=t.descripcion,
            prioridad=t.prioridad,
            estado=t.estado,
            created_at=t.created_at,
            updated_at=t.updated_at
        )
        for t in tickets
    ]


@router.get("/{ticket_id}", response_model=TicketResponse)
def obtener_ticket(
    ticket_id: int,
    ticket_repo: ITicketRepository = Depends(get_ticket_repository)
):
    """
    Obtiene un ticket por su ID.
    """
    use_case = ObtenerTicketUseCase(ticket_repo)
    ticket = use_case.ejecutar(ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket con ID {ticket_id} no encontrado"
        )
    
    return TicketResponse(
        ticket_id=ticket.ticket_id,
        usuario_id=ticket.usuario_id,
        tecnico_id=ticket.tecnico_id,
        descripcion=ticket.descripcion,
        prioridad=ticket.prioridad,
        estado=ticket.estado,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at
    )


@router.put("/{ticket_id}", response_model=TicketResponse)
def actualizar_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    ticket_repo: ITicketRepository = Depends(get_ticket_repository)
):
    """
    Actualiza un ticket existente.
    
    Puedes actualizar:
    - **descripcion**: Nueva descripción
    - **prioridad**: Nueva prioridad
    - **estado**: Nuevo estado
    """
    try:
        use_case_obtener = ObtenerTicketUseCase(ticket_repo)
        ticket = use_case_obtener.ejecutar(ticket_id)
        
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket con ID {ticket_id} no encontrado"
            )
        
        # Actualizar campos según lo proporcionado
        if ticket_data.descripcion is not None:
            ticket.actualizar_descripcion(ticket_data.descripcion)
        
        if ticket_data.prioridad is not None:
            use_case_prioridad = ActualizarPrioridadTicketUseCase(ticket_repo)
            ticket = use_case_prioridad.ejecutar(ticket_id, ticket_data.prioridad)
        
        if ticket_data.estado is not None:
            use_case_estado = ActualizarEstadoTicketUseCase(ticket_repo)
            ticket = use_case_estado.ejecutar(ticket_id, ticket_data.estado)
        
        # Si solo se actualizó descripción, guardar cambios
        if ticket_data.descripcion is not None and ticket_data.prioridad is None and ticket_data.estado is None:
            ticket = ticket_repo.actualizar(ticket)
        
        return TicketResponse(
            ticket_id=ticket.ticket_id,
            usuario_id=ticket.usuario_id,
            tecnico_id=ticket.tecnico_id,
            descripcion=ticket.descripcion,
            prioridad=ticket.prioridad,
            estado=ticket.estado,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{ticket_id}/asignar-tecnico", response_model=TicketResponse)
def asignar_tecnico(
    ticket_id: int,
    request: AsignarTecnicoRequest,
    ticket_repo: ITicketRepository = Depends(get_ticket_repository),
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
):
    """
    Asigna un técnico a un ticket.
    
    - **tecnico_id**: ID del técnico a asignar
    """
    try:
        use_case = AsignarTecnicoUseCase(ticket_repo, usuario_repo)
        ticket = use_case.ejecutar(ticket_id, request.tecnico_id)
        
        return TicketResponse(
            ticket_id=ticket.ticket_id,
            usuario_id=ticket.usuario_id,
            tecnico_id=ticket.tecnico_id,
            descripcion=ticket.descripcion,
            prioridad=ticket.prioridad,
            estado=ticket.estado,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/reporte/prioridad/{prioridad}", response_model=List[TicketResponse])
def reporte_por_prioridad(
    prioridad: Prioridad,
    ticket_repo: ITicketRepository = Depends(get_ticket_repository)
):
    """
    Genera un reporte de tickets filtrados por prioridad.
    
    - **prioridad**: baja, media, alta, critica
    """
    use_case = GenerarReportePorPrioridadUseCase(ticket_repo)
    tickets = use_case.ejecutar(prioridad)
    
    return [
        TicketResponse(
            ticket_id=t.ticket_id,
            usuario_id=t.usuario_id,
            tecnico_id=t.tecnico_id,
            descripcion=t.descripcion,
            prioridad=t.prioridad,
            estado=t.estado,
            created_at=t.created_at,
            updated_at=t.updated_at
        )
        for t in tickets
    ]


@router.get("/reporte/estado/{estado}", response_model=List[TicketResponse])
def reporte_por_estado(
    estado: Estado,
    ticket_repo: ITicketRepository = Depends(get_ticket_repository)
):
    """
    Genera un reporte de tickets filtrados por estado.
    
    - **estado**: abierto, en_proceso, cerrado
    """
    use_case = GenerarReportePorEstadoUseCase(ticket_repo)
    tickets = use_case.ejecutar(estado)
    
    return [
        TicketResponse(
            ticket_id=t.ticket_id,
            usuario_id=t.usuario_id,
            tecnico_id=t.tecnico_id,
            descripcion=t.descripcion,
            prioridad=t.prioridad,
            estado=t.estado,
            created_at=t.created_at,
            updated_at=t.updated_at
        )
        for t in tickets
    ]


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ticket(
    ticket_id: int,
    ticket_repo: ITicketRepository = Depends(get_ticket_repository)
):
    """
    Elimina un ticket por su ID.
    """
    try:
        use_case = EliminarTicketUseCase(ticket_repo)
        resultado = use_case.ejecutar(ticket_id)
        
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket con ID {ticket_id} no encontrado"
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

