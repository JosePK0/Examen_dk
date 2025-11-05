from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from domain.ports.usuario_repository import IUsuarioRepository
from domain.entities.usuario import Usuario
from domain.entities.ticket import Rol
from api.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from api.dependencies import get_usuario_repository

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario_data: UsuarioCreate,
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
):
    """
    Crea un nuevo usuario.
    
    - **nombre**: Nombre del usuario
    - **correo**: Correo electrónico (único)
    - **contrasena**: Contraseña del usuario
    - **rol**: Rol del usuario (usuario, tecnico, admin)
    """
    try:
        # Verificar si el correo ya existe
        usuario_existente = usuario_repo.obtener_por_correo(usuario_data.correo)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El correo {usuario_data.correo} ya está registrado"
            )
        
        # Crear usuario
        usuario = Usuario(
            nombre=usuario_data.nombre,
            correo=usuario_data.correo,
            contrasena=usuario_data.contrasena,  # En producción, debería estar hasheada
            rol=usuario_data.rol
        )
        
        usuario_creado = usuario_repo.crear(usuario)
        
        return UsuarioResponse(
            usuario_id=usuario_creado.usuario_id,
            nombre=usuario_creado.nombre,
            correo=usuario_creado.correo,
            rol=usuario_creado.rol,
            activo=usuario_creado.activo,
            created_at=usuario_creado.created_at,
            updated_at=usuario_creado.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
):
    """
    Lista todos los usuarios.
    """
    usuarios = usuario_repo.obtener_todos()
    
    return [
        UsuarioResponse(
            usuario_id=u.usuario_id,
            nombre=u.nombre,
            correo=u.correo,
            rol=u.rol,
            activo=u.activo,
            created_at=u.created_at,
            updated_at=u.updated_at
        )
        for u in usuarios
    ]


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int,
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
):
    """
    Obtiene un usuario por su ID.
    """
    usuario = usuario_repo.obtener_por_id(usuario_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    
    return UsuarioResponse(
        usuario_id=usuario.usuario_id,
        nombre=usuario.nombre,
        correo=usuario.correo,
        rol=usuario.rol,
        activo=usuario.activo,
        created_at=usuario.created_at,
        updated_at=usuario.updated_at
    )


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
):
    """
    Actualiza un usuario existente.
    """
    try:
        usuario = usuario_repo.obtener_por_id(usuario_id)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )
        
        # Verificar si el correo ya existe en otro usuario (solo si se está cambiando)
        if usuario_data.correo is not None and usuario_data.correo != usuario.correo:
            usuario_con_correo = usuario_repo.obtener_por_correo(usuario_data.correo)
            if usuario_con_correo and usuario_con_correo.usuario_id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El correo {usuario_data.correo} ya está registrado en otro usuario"
                )
        
        # Actualizar datos (solo los campos proporcionados)
        if usuario_data.nombre is not None:
            usuario.nombre = usuario_data.nombre
        if usuario_data.correo is not None:
            usuario.correo = usuario_data.correo
        if usuario_data.rol is not None:
            usuario.rol = usuario_data.rol
        if usuario_data.contrasena is not None:
            usuario.contrasena = usuario_data.contrasena
        
        usuario_actualizado = usuario_repo.actualizar(usuario)
        
        return UsuarioResponse(
            usuario_id=usuario_actualizado.usuario_id,
            nombre=usuario_actualizado.nombre,
            correo=usuario_actualizado.correo,
            rol=usuario_actualizado.rol,
            activo=usuario_actualizado.activo,
            created_at=usuario_actualizado.created_at,
            updated_at=usuario_actualizado.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int,
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
):
    """
    Elimina un usuario por su ID.
    """
    usuario = usuario_repo.obtener_por_id(usuario_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    
    resultado = usuario_repo.eliminar(usuario_id)
    
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al eliminar el usuario"
        )


@router.get("/tecnicos/list", response_model=List[UsuarioResponse])
def listar_tecnicos(
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
):
    """
    Lista todos los técnicos disponibles.
    """
    tecnicos = usuario_repo.obtener_tecnicos()
    
    return [
        UsuarioResponse(
            usuario_id=t.usuario_id,
            nombre=t.nombre,
            correo=t.correo,
            rol=t.rol,
            activo=t.activo,
            created_at=t.created_at,
            updated_at=t.updated_at
        )
        for t in tecnicos
    ]

