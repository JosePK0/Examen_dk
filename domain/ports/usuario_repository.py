from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.usuario import Usuario


class IUsuarioRepository(ABC):
    """Puerto (interfaz) para el repositorio de usuarios"""
    
    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        """Obtiene un usuario por su correo"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        pass
    
    @abstractmethod
    def obtener_tecnicos(self) -> List[Usuario]:
        """Obtiene todos los técnicos"""
        pass
    
    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente"""
        pass
    
    @abstractmethod
    def eliminar(self, usuario_id: int) -> bool:
        """Elimina un usuario"""
        pass

