# HelpDeskPro - Sistema de Gestión de Incidencias

**Versión:** 1.0.0  
**Fecha:** 2025  
**Arquitectura:** Hexagonal (Ports & Adapters)  
**Framework:** FastAPI  
**Base de Datos:** MySQL

Sistema completo de gestión de tickets con arquitectura hexagonal (Ports & Adapters) implementado en FastAPI.

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura Hexagonal](#arquitectura-hexagonal)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Dependency Injection](#dependency-injection)
5. [Flujo de Datos](#flujo-de-datos)
6. [Instalación y Configuración](#instalación-y-configuración)
7. [Endpoints Disponibles](#endpoints-disponibles)
8. [Implementación Funcional](#implementación-funcional)
9. [Diagramas UML](#diagramas-uml)
10. [Cumplimiento de Requisitos](#cumplimiento-de-requisitos)
11. [Guía de Uso](#guía-de-uso)
12. [Principios de Diseño](#principios-de-diseño)

---

## 1. Introducción

HelpDeskPro es un sistema de gestión de incidencias desarrollado con **Arquitectura Hexagonal** (también conocida como **Ports & Adapters**), que permite gestionar tickets de soporte técnico, asignar técnicos y generar reportes.

### Características Principales

- ✅ CRUD completo de tickets y usuarios
- ✅ Asignación de técnicos a tickets
- ✅ Gestión de estados y prioridades
- ✅ Generación de reportes
- ✅ Validaciones de negocio
- ✅ Lógica desacoplada del acceso a datos
- ✅ Dependency Injection implementado
- ✅ Arquitectura Hexagonal completa

---

## 2. Arquitectura Hexagonal

### 2.1 Conceptos Fundamentales

La **Arquitectura Hexagonal** (también llamada **Ports & Adapters**) separa la aplicación en:
- **Núcleo (Domain)**: Lógica de negocio independiente
- **Periferia (Infrastructure/API)**: Detalles técnicos y adaptadores

### ¿Por qué se llama "Hexagonal"?

No significa que tenga 6 lados, sino que el hexágono representa que el dominio puede tener múltiples adaptadores (API REST, GraphQL, CLI, pruebas, etc.) sin cambiar el núcleo.

### 2.2 Separación de Capas

#### Capa Interna (Dominio)

```
domain/
├── entities/          # Entidades de negocio (Ticket, Usuario)
├── ports/            # Interfaces (ITicketRepository, IUsuarioRepository)
└── use_cases/        # Casos de uso (lógica de negocio)
```

**Características:**
- ✅ **NO** depende de frameworks
- ✅ **NO** depende de base de datos
- ✅ **NO** depende de APIs
- ✅ Contiene SOLO lógica de negocio pura

#### Capa Externa (Infraestructura)

```
infrastructure/
├── database/         # Configuración de BD y modelos ORM
└── repositories/     # Implementaciones de repositorios
```

**Características:**
- ✅ Implementa las interfaces del dominio
- ✅ Maneja detalles técnicos (SQLAlchemy, MySQL)
- ✅ Puede ser reemplazada sin afectar el dominio

#### Capa de Aplicación (API)

```
api/
├── routes.py         # Endpoints REST
├── schemas.py        # DTOs (Data Transfer Objects)
└── dependencies.py   # Inyección de dependencias
```

**Características:**
- ✅ Adaptador de entrada (HTTP REST)
- ✅ Transforma requests HTTP en llamadas al dominio
- ✅ Transforma entidades en responses HTTP

### 2.3 Puertos (Ports) - Las Interfaces

Un **Puerto** es una **interfaz** que define un **contrato** sin implementación. Es como un "enchufe" que define qué operaciones se pueden hacer.

#### Ejemplo: ITicketRepository

```python
# domain/ports/ticket_repository.py
from abc import ABC, abstractmethod

class ITicketRepository(ABC):  # ← PUERTO (Interfaz)
    """Puerto: Define QUÉ operaciones se pueden hacer"""
    
    @abstractmethod
    def crear(self, ticket: Ticket) -> Ticket:
        """Crea un ticket"""
        pass  # ← No tiene implementación, solo define el contrato
    
    @abstractmethod
    def obtener_por_id(self, ticket_id: int) -> Optional[Ticket]:
        """Obtiene un ticket por ID"""
        pass
```

**Características del Puerto:**
- Define **QUÉ** se puede hacer
- **NO** define **CÓMO** se hace
- El dominio **solo** conoce el puerto, no la implementación

### 2.4 Adaptadores (Adapters) - Las Implementaciones

Un **Adaptador** es una **implementación concreta** de un puerto. Es como un "cable" que conecta el puerto con una tecnología específica.

#### Ejemplo: TicketRepository

```python
# infrastructure/repositories/ticket_repository.py
from domain.ports.ticket_repository import ITicketRepository

class TicketRepository(ITicketRepository):  # ← ADAPTADOR (Implementación)
    """Adaptador: Implementa CÓMO se hacen las operaciones con SQLAlchemy"""
    
    def __init__(self, session: Session):
        self._session = session  # ← Dependencia de SQLAlchemy
    
    def crear(self, ticket: Ticket) -> Ticket:
        """Implementación concreta usando SQLAlchemy"""
        model = self._to_model(ticket)  # Entidad → Modelo ORM
        self._session.add(model)         # SQLAlchemy
        self._session.commit()           # MySQL
        return self._to_entity(model)    # Modelo ORM → Entidad
```

**Características del Adaptador:**
- Implementa **CÓMO** se hace
- Conoce detalles técnicos (SQLAlchemy, MySQL)
- Puede ser reemplazado sin afectar el dominio

### 2.5 Ventajas de la Arquitectura Hexagonal

1. **Independencia del Dominio**: El dominio no depende de tecnologías externas
2. **Testabilidad**: Fácil de testear con mocks de los puertos
3. **Mantenibilidad**: Cambios en infraestructura no afectan el dominio
4. **Flexibilidad**: Cambiar de MySQL a PostgreSQL solo requiere cambiar adaptadores

### 2.6 Reglas de Dependencia

```
Las dependencias apuntan HACIA ADENTRO (hacia el dominio)

API → Domain ← Infrastructure
```

**Reglas:**
1. ✅ API depende de Domain
2. ✅ Infrastructure depende de Domain
3. ❌ Domain NO depende de API
4. ❌ Domain NO depende de Infrastructure
5. ❌ API NO depende directamente de Infrastructure

---

## 3. Estructura del Proyecto

```
Examen_dk/
├── api/                          # Capa de Aplicación (Adaptador de Entrada)
│   ├── dependencies.py          # Inyección de dependencias
│   ├── routes.py                # Endpoints de tickets
│   ├── usuario_routes.py        # Endpoints de usuarios
│   └── schemas.py               # DTOs (Data Transfer Objects)
│
├── domain/                       # Capa de Dominio (Núcleo)
│   ├── entities/                 # Entidades de negocio
│   │   ├── ticket.py            # Entidad Ticket
│   │   └── usuario.py           # Entidad Usuario
│   ├── ports/                    # Interfaces (Puertos)
│   │   ├── ticket_repository.py # ITicketRepository
│   │   └── usuario_repository.py# IUsuarioRepository
│   └── use_cases/                # Casos de uso
│       └── ticket_use_cases.py  # Lógica de negocio
│
├── infrastructure/               # Capa de Infraestructura (Adaptadores)
│   ├── database/                 # Configuración de BD
│   │   ├── config.py            # Conexión y sesión
│   │   └── models.py            # Modelos ORM
│   └── repositories/             # Implementaciones
│       ├── ticket_repository.py # TicketRepository (SQLAlchemy)
│       └── usuario_repository.py# UsuarioRepository (SQLAlchemy)
│
├── main.py                       # Punto de entrada
├── requirements.txt              # Dependencias
├── database_init.sql            # Script de inicialización
└── README.md                     # Este archivo
```

---

## 4. Dependency Injection

### 4.1 Implementación

El sistema utiliza **Dependency Injection** a través de FastAPI's `Depends()` para inyectar dependencias en los endpoints.

#### Flujo de Inyección

```python
# 1. Definición de dependencias (api/dependencies.py)
def get_ticket_repository(db: Session = Depends(get_db_session)) -> ITicketRepository:
    return TicketRepository(db)

# 2. Uso en endpoints (api/routes.py)
@router.post("/")
def crear_ticket(
    ticket_data: TicketCreate,
    ticket_repo: ITicketRepository = Depends(get_ticket_repository)
):
    use_case = CrearTicketUseCase(ticket_repo, usuario_repo)
    ticket = use_case.ejecutar(...)
```

#### Inyección en Casos de Uso

```python
# Caso de uso recibe interfaz, no implementación
class CrearTicketUseCase:
    def __init__(self, ticket_repo: ITicketRepository, usuario_repo: IUsuarioRepository):
        self._ticket_repo = ticket_repo  # ← Dependencia inyectada
        self._usuario_repo = usuario_repo  # ← Dependencia inyectada
```

### 4.2 Beneficios del Dependency Injection

1. **Desacoplamiento**: Los casos de uso no conocen implementaciones concretas
2. **Testabilidad**: Fácil inyectar mocks en tests
3. **Flexibilidad**: Cambiar implementaciones sin modificar código cliente
4. **Mantenibilidad**: Código más limpio y organizado

### 4.3 Ejemplo de Testing con Mocks

```python
# Fácil crear mocks para testing
class MockTicketRepository(ITicketRepository):
    def crear(self, ticket):
        return ticket  # ← Simula BD sin usar BD real

def test_crear_ticket():
    mock_repo = MockTicketRepository()
    use_case = CrearTicketUseCase(mock_repo)
    ticket = use_case.ejecutar(1, "Problema", Prioridad.ALTA)
    assert ticket.descripcion == "Problema"
```

---

## 5. Flujo de Datos

### 5.1 Flujo Completo: Cliente → API → Dominio → Infraestructura → BD

```
┌─────────┐
│ Cliente │  (HTTP Request)
└────┬────┘
     │
     │ 1. POST /api/tickets/
     ▼
┌─────────────────────────────────────────────┐
│         API Layer (Adaptador Entrada)      │
│  ┌──────────────────────────────────────┐  │
│  │  routes.py                            │  │
│  │  def crear_ticket(ticket_data):       │  │
│  │      # Validar con Pydantic          │  │
│  │      # Inyectar dependencias         │  │
│  │      use_case = CrearTicketUseCase() │  │
│  └──────────────┬───────────────────────┘  │
└─────────────────┼───────────────────────────┘
                  │
                  │ 2. Llamar caso de uso
                  ▼
┌─────────────────────────────────────────────┐
│      Domain Layer (Núcleo de Negocio)      │
│  ┌──────────────────────────────────────┐  │
│  │  CrearTicketUseCase                   │  │
│  │  def ejecutar(usuario_id, descripcion):│ │
│  │      # Validar usuario existe        │  │
│  │      # Crear entidad Ticket          │  │
│  │      ticket = Ticket(...)            │  │
│  │      # Llamar al PUERTO (interfaz)  │  │
│  │      return repo.crear(ticket)       │  │
│  │      # ← NO conoce SQLAlchemy!      │  │
│  └──────────────┬───────────────────────┘  │
└─────────────────┼───────────────────────────┘
                  │
                  │ 3. Usa interfaz (Puerto)
                  ▼
┌─────────────────────────────────────────────┐
│    Port (Interface) - Solo Contrato        │
│  ┌──────────────────────────────────────┐  │
│  │  ITicketRepository                    │  │
│  │  def crear(ticket): Ticket            │  │
│  │      # ← Solo definición, sin código │  │
│  └──────────────┬───────────────────────┘  │
└─────────────────┼───────────────────────────┘
                  │
                  │ 4. Implementado por Adaptador
                  ▼
┌─────────────────────────────────────────────┐
│  Infrastructure Layer (Adaptador Salida)    │
│  ┌──────────────────────────────────────┐  │
│  │  TicketRepository                     │  │
│  │  def crear(self, ticket):             │  │
│  │      model = _to_model(ticket)        │  │
│  │      self._session.add(model)         │  │
│  │      self._session.commit()          │  │
│  │      # ← Conoce SQLAlchemy y MySQL   │  │
│  └──────────────┬───────────────────────┘  │
└─────────────────┼───────────────────────────┘
                  │
                  │ 5. Guardar en BD
                  ▼
┌─────────────────────────────────────────────┐
│           Database (MySQL)                   │
│  ┌──────────────────────────────────────┐  │
│  │  INSERT INTO tickets (...)            │  │
│  │  VALUES (...)                         │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 5.2 Flujo de Creación de Ticket (Paso a Paso)

```
1. Cliente HTTP → API Endpoint
   POST /api/tickets/
   
2. API → Schema Validation
   TicketCreate (Pydantic)
   
3. API → Dependency Injection
   get_ticket_repository() → TicketRepository
   get_usuario_repository() → UsuarioRepository
   
4. API → Use Case
   CrearTicketUseCase.ejecutar()
   
5. Use Case → Validaciones de Negocio
   - Verificar usuario existe
   - Verificar usuario activo
   - Validar descripción
   
6. Use Case → Entity
   Ticket(usuario_id, descripcion, prioridad)
   
7. Use Case → Repository (Port)
   ticket_repo.crear(ticket)
   
8. Repository → Adapter (Infrastructure)
   TicketRepository._to_model() → TicketModel
   
9. Adapter → Database
   SQLAlchemy Session → MySQL
   
10. Database → Response
    TicketModel → Ticket Entity → TicketResponse
```

### 5.3 Flujo de Asignación de Técnico

```
1. Cliente HTTP → API Endpoint
   POST /api/tickets/{id}/asignar-tecnico
   
2. API → Dependency Injection
   get_ticket_repository() → TicketRepository
   get_usuario_repository() → UsuarioRepository
   
3. API → Use Case
   AsignarTecnicoUseCase.ejecutar(ticket_id, tecnico_id)
   
4. Use Case → Validaciones
   - Ticket existe?
   - Técnico existe?
   - Es técnico?
   - Técnico activo?
   
5. Use Case → Entity Method
   ticket.asignar_tecnico(tecnico_id)
   
6. Entity → Business Logic
   - Cambia estado a EN_PROCESO si estaba ABIERTO
   - Actualiza tecnico_id
   
7. Use Case → Repository
   ticket_repo.actualizar(ticket)
   
8. Repository → Database
   UPDATE tickets SET tecnicoID = ?, estado = ? WHERE IDticket = ?
```

---

## 6. Instalación y Configuración

### 6.1 Requisitos Previos

- Python 3.8+
- MySQL 5.7+
- pip (gestor de paquetes de Python)

### 6.2 Pasos de Instalación

1. **Clonar o navegar al proyecto:**
```bash
cd Examen_dk
```

2. **Crear un entorno virtual:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos:**
   - Crear la base de datos `helpdesk_db` en MySQL
   - Ejecutar los scripts SQL proporcionados para crear las tablas
   - Copiar `config.env.example` a `.env` y configurar las credenciales

5. **Ejecutar la aplicación:**
```bash
python main.py
```

O con uvicorn directamente:
```bash
uvicorn main:app --reload
```

### 6.3 Configuración de Variables de Entorno

Crear archivo `.env` basado en `config.env.example`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=helpdesk_db
```

---

## 7. Endpoints Disponibles

### 7.1 Tickets

- `POST /api/tickets/` - Crear un nuevo ticket
- `GET /api/tickets/` - Listar todos los tickets
- `GET /api/tickets/{ticket_id}` - Obtener un ticket por ID
- `PUT /api/tickets/{ticket_id}` - Actualizar un ticket
- `POST /api/tickets/{ticket_id}/asignar-tecnico` - Asignar técnico a un ticket
- `GET /api/tickets/reporte/prioridad/{prioridad}` - Reporte por prioridad
- `GET /api/tickets/reporte/estado/{estado}` - Reporte por estado
- `DELETE /api/tickets/{ticket_id}` - Eliminar un ticket

### 7.2 Usuarios

- `POST /api/usuarios/` - Crear usuario
- `GET /api/usuarios/` - Listar todos
- `GET /api/usuarios/{id}` - Obtener por ID
- `PUT /api/usuarios/{id}` - Actualizar usuario
- `DELETE /api/usuarios/{id}` - Eliminar usuario
- `GET /api/usuarios/tecnicos/list` - Listar técnicos

### 7.3 Documentación

- `GET /docs` - Documentación interactiva (Swagger UI)
- `GET /redoc` - Documentación alternativa (ReDoc)

---

## 8. Implementación Funcional

### 8.1 CRUD Completo de Tickets

#### **Create (Crear)**
- **Endpoint**: `POST /api/tickets/`
- **Use Case**: `CrearTicketUseCase`
- **Validaciones**:
  - Usuario existe y está activo
  - Descripción no vacía (mínimo 10 caracteres)
  - Prioridad válida

#### **Read (Leer)**
- **Listar todos**: `GET /api/tickets/` → `ListarTicketsUseCase`
- **Obtener por ID**: `GET /api/tickets/{id}` → `ObtenerTicketUseCase`
- **Por prioridad**: `GET /api/tickets/reporte/prioridad/{prioridad}`
- **Por estado**: `GET /api/tickets/reporte/estado/{estado}`

#### **Update (Actualizar)**
- **Endpoint**: `PUT /api/tickets/{id}`
- **Use Cases**:
  - `ActualizarEstadoTicketUseCase`
  - `ActualizarPrioridadTicketUseCase`
- **Validaciones**:
  - No cerrar ticket sin estar en proceso
  - Estados válidos según transiciones

#### **Delete (Eliminar)**
- **Endpoint**: `DELETE /api/tickets/{id}`
- **Use Case**: `EliminarTicketUseCase`

### 8.2 CRUD Completo de Usuarios

#### **Create (Crear)**
- **Endpoint**: `POST /api/usuarios/`
- **Validaciones**:
  - Correo único
  - Contraseña mínima 6 caracteres
  - Nombre válido (solo letras)

#### **Read (Leer)**
- **Listar todos**: `GET /api/usuarios/`
- **Obtener por ID**: `GET /api/usuarios/{id}`
- **Listar técnicos**: `GET /api/usuarios/tecnicos/list`

#### **Update (Actualizar)**
- **Endpoint**: `PUT /api/usuarios/{id}`
- **Validaciones**: Correo único (si se actualiza)

#### **Delete (Eliminar)**
- **Endpoint**: `DELETE /api/usuarios/{id}`

### 8.3 Lógica Desacoplada del Acceso a Datos

#### Ejemplo: CrearTicketUseCase

```python
class CrearTicketUseCase:
    def __init__(self, ticket_repo: ITicketRepository, usuario_repo: IUsuarioRepository):
        # ← Recibe interfaces, no implementaciones
        self._ticket_repo = ticket_repo
        self._usuario_repo = usuario_repo
    
    def ejecutar(self, usuario_id: int, descripcion: str, prioridad: Prioridad):
        # ← Lógica de negocio pura, sin SQL ni ORM
        usuario = self._usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no existe")
        
        ticket = Ticket(usuario_id=usuario_id, descripcion=descripcion, prioridad=prioridad)
        return self._ticket_repo.crear(ticket)
```

**Ventajas**:
- ✅ El caso de uso no conoce SQL
- ✅ Fácil cambiar de MySQL a PostgreSQL
- ✅ Testeable con mocks

### 8.4 Validaciones y Gestión de Estados

#### Validaciones en Entidades

```python
class Ticket:
    def asignar_tecnico(self, tecnico_id: int):
        if self.estado == Estado.CERRADO:
            raise ValueError("No se puede asignar técnico a ticket cerrado")
        self.tecnico_id = tecnico_id
        if self.estado == Estado.ABIERTO:
            self.estado = Estado.EN_PROCESO
```

#### Validaciones en Casos de Uso

```python
class CrearTicketUseCase:
    def ejecutar(self, usuario_id: int, descripcion: str, prioridad: Prioridad):
        # Validar usuario existe
        usuario = self._usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no existe")
        
        # Validar usuario activo
        if not usuario.activo:
            raise ValueError("Usuario no está activo")
        
        # Validar descripción
        if not descripcion or not descripcion.strip():
            raise ValueError("Descripción no puede estar vacía")
```

#### Validaciones en API (Pydantic)

```python
class TicketCreate(BaseModel):
    usuario_id: int = Field(..., gt=0)  # ← Debe ser > 0
    descripcion: str = Field(..., min_length=10, max_length=2000)  # ← Validación
    prioridad: Prioridad = Field(default=Prioridad.MEDIA)
    
    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v):
        if not v.strip() or len(v.strip()) < 10:
            raise ValueError('La descripción debe tener al menos 10 caracteres')
        return v.strip()
```

#### Transiciones de Estado

```
✅ ABIERTO → EN_PROCESO (al asignar técnico)
✅ EN_PROCESO → CERRADO (al cerrar)
❌ ABIERTO → CERRADO (NO permitido)
❌ CERRADO → cualquier estado (NO permitido)
```

---

## 9. Diagramas UML

### 9.1 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        API LAYER                                │
│                    (Adaptador de Entrada)                       │
│                                                                 │
│  ┌────────────────────┐      ┌────────────────────┐          │
│  │   routes.py         │      │ usuario_routes.py │          │
│  │  - crear_ticket     │      │  - crear_usuario   │          │
│  │  - listar_tickets   │      │  - listar_usuarios │          │
│  │  - asignar_tecnico  │      │  - actualizar      │          │
│  └──────────┬──────────┘      └──────────┬─────────┘          │
│             │                           │                    │
│             └───────────┬─────────────────┘                    │
│                        ▼                                      │
│              ┌────────────────────┐                           │
│              │  dependencies.py   │                           │
│              │  - get_ticket_repo  │                           │
│              │  - get_usuario_repo │                           │
│              └──────────┬─────────┘                           │
└─────────────────────────┼─────────────────────────────────────┘
                         │ uses
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DOMAIN LAYER                              │
│                    (Núcleo de Negocio)                         │
│                                                                 │
│  ┌────────────────────┐      ┌────────────────────┐          │
│  │   Use Cases        │      │     Entities        │          │
│  │                    │      │                     │          │
│  │ CrearTicketUseCase │      │      Ticket         │          │
│  │ AsignarTecnicoUC   │      │      Usuario         │          │
│  │ ActualizarEstadoUC │      │                     │          │
│  │ ListarTicketsUC    │      │                     │          │
│  └──────────┬─────────┘      └──────────┬─────────┘          │
│             │                           │                    │
│             │ uses                       │                    │
│             │                           │                    │
│             └───────────┬────────────────┘                    │
│                        ▼                                      │
│              ┌────────────────────┐                           │
│              │      Ports         │                           │
│              │  (Interfaces)       │                           │
│              │                    │                           │
│              │ ITicketRepository  │                           │
│              │ IUsuarioRepository │                           │
│              └──────────┬─────────┘                           │
└─────────────────────────┼─────────────────────────────────────┘
                         │ implements
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                            │
│                    (Adaptadores)                                │
│                                                                 │
│  ┌────────────────────┐      ┌────────────────────┐          │
│  │   Repositories     │      │     Database       │          │
│  │                    │      │                     │          │
│  │ TicketRepository   │      │   TicketModel       │          │
│  │ UsuarioRepository  │      │   UsuarioModel      │          │
│  │                    │      │   SQLAlchemy        │          │
│  └──────────┬─────────┘      └──────────┬─────────┘          │
│             │                           │                    │
│             └───────────┬───────────────┘                    │
│                        ▼                                      │
│              ┌────────────────────┐                           │
│              │      MySQL         │                           │
│              │   helpdeskpro     │                           │
│              └───────────────────┘                           │
└───────────────────────────────────────────────────────────────┘
```

### 9.2 Diagrama de Clases - Entidades

```
┌─────────────────────────────────────┐
│            Ticket                   │
├─────────────────────────────────────┤
│ - ticket_id: int                    │
│ - usuario_id: int                   │
│ - tecnico_id: Optional[int]          │
│ - descripcion: str                  │
│ - prioridad: Prioridad               │
│ - estado: Estado                     │
│ - created_at: datetime                │
│ - updated_at: datetime                │
├─────────────────────────────────────┤
│ + asignar_tecnico(tecnico_id)       │
│ + actualizar_estado(estado)         │
│ + actualizar_prioridad(prioridad)   │
│ + actualizar_descripcion(desc)       │
└─────────────────────────────────────┘
              │
              │ uses
              ▼
┌─────────────────────────────────────┐
│          Prioridad (Enum)            │
├─────────────────────────────────────┤
│ BAJA                                 │
│ MEDIA                                │
│ ALTA                                 │
│ CRITICA                              │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│          Estado (Enum)               │
├─────────────────────────────────────┤
│ ABIERTO                              │
│ EN_PROCESO                           │
│ CERRADO                              │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Usuario                   │
├─────────────────────────────────────┤
│ - usuario_id: int                    │
│ - nombre: str                         │
│ - correo: str                         │
│ - contrasena: str                     │
│ - rol: Rol                            │
│ - activo: bool                        │
│ - created_at: datetime                │
│ - updated_at: datetime                │
├─────────────────────────────────────┤
│ + es_tecnico(): bool                 │
│ + es_admin(): bool                   │
│ + es_usuario(): bool                 │
└─────────────────────────────────────┘
              │
              │ uses
              ▼
┌─────────────────────────────────────┐
│           Rol (Enum)                │
├─────────────────────────────────────┤
│ USUARIO                              │
│ TECNICO                              │
│ ADMIN                                │
└─────────────────────────────────────┘
```

### 9.3 Diagrama de Clases - Repositorios

```
┌─────────────────────────────────────────────┐
│      ITicketRepository <<interface>>       │
├─────────────────────────────────────────────┤
│ + crear(ticket): Ticket                    │
│ + obtener_por_id(id): Optional[Ticket]     │
│ + obtener_todos(): List[Ticket]            │
│ + obtener_por_usuario(id): List[Ticket]     │
│ + obtener_por_tecnico(id): List[Ticket]    │
│ + obtener_por_prioridad(p): List[Ticket]    │
│ + obtener_por_estado(e): List[Ticket]      │
│ + actualizar(ticket): Ticket               │
│ + eliminar(id): bool                       │
└─────────────────────────────────────────────┘
                    ▲
                    │ implements
                    │
┌─────────────────────────────────────────────┐
│        TicketRepository                      │
├─────────────────────────────────────────────┤
│ - _session: Session                          │
├─────────────────────────────────────────────┤
│ + crear(ticket): Ticket                     │
│ + obtener_por_id(id): Optional[Ticket]      │
│ + obtener_todos(): List[Ticket]            │
│ + actualizar(ticket): Ticket                │
│ + eliminar(id): bool                        │
│ - _to_entity(model): Ticket                 │
│ - _to_model(entity): TicketModel            │
└─────────────────────────────────────────────┘
```

### 9.4 Diagrama de Secuencia - Crear Ticket

```
┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐
│ Cliente │  │   API  │  │Use Case │  │TicketRepo│  │UsuarioRepo│ │Database │
└────┬────┘  └────┬───┘  └────┬────┘  └────┬─────┘  └────┬─────┘  └────┬────┘
     │            │            │            │              │             │
     │ POST       │            │            │              │             │
     │ /tickets/  │            │            │              │             │
     ├───────────>│            │            │              │             │
     │            │            │            │              │             │
     │            │ Dependency │            │              │             │
     │            │ Injection  │            │              │             │
     │            ├───────────>│            │              │             │
     │            │            │            │              │             │
     │            │ ejecutar(  │            │              │             │
     │            │ usuario_id, │            │              │             │
     │            │ descripcion)│            │              │             │
     │            ├───────────>│            │              │             │
     │            │            │            │              │             │
     │            │            │ obtener_   │              │             │
     │            │            │ por_id()   │              │             │
     │            │            ├───────────>│              │             │
     │            │            │            │ SELECT       │             │
     │            │            │            ├──────────────>│             │
     │            │            │            │              │             │
     │            │            │            │              │ SELECT      │
     │            │            │            │              ├─────────────>│
     │            │            │            │              │<─────────────│
     │            │            │            │<─────────────│             │
     │            │            │<───────────│              │             │
     │            │            │ Usuario    │              │             │
     │            │            │            │              │             │
     │            │            │ Validar    │              │             │
     │            │            │ usuario    │              │             │
     │            │            │            │              │             │
     │            │            │ crear()    │              │             │
     │            │            ├───────────>│              │             │
     │            │            │            │ _to_model()  │             │
     │            │            │            │ INSERT       │             │
     │            │            │            ├──────────────>│             │
     │            │            │            │              │             │
     │            │            │            │<─────────────│             │
     │            │            │<───────────│ TicketModel  │             │
     │            │            │ Ticket     │              │             │
     │            │<───────────│            │              │             │
     │            │ Ticket     │            │              │             │
     │<───────────│            │            │              │             │
     │ Response   │            │            │              │             │
```

### 9.5 Diagrama de Estados - Ticket

```
┌─────────────┐
│   ABIERTO   │
│             │
│ tecnico_id  │
│ = None      │
└──────┬──────┘
       │
       │ asignar_tecnico()
       │
       ▼
┌─────────────────┐
│  EN_PROCESO      │
│                  │
│ tecnico_id       │
│ != None          │
└──────┬───────────┘
       │
       │ actualizar_estado(CERRADO)
       │
       ▼
┌─────────────┐
│   CERRADO    │
│              │
│ (No se puede │
│  modificar)  │
└─────────────┘

Transiciones:
- ABIERTO → EN_PROCESO: Al asignar técnico
- EN_PROCESO → CERRADO: Al cerrar ticket
- ❌ ABIERTO → CERRADO: NO permitido
- ❌ CERRADO → cualquier estado: NO permitido
```

---

## 10. Cumplimiento de Requisitos

### ✅ 1. Diseño de la Arquitectura Hexagonal (Ports & Adapters)

#### 1.1 Separar la aplicación en capas internas (dominio) y externas (infraestructura)

**✅ CUMPLIDO**

**Estructura de Capas:**

```
📁 domain/                    ← CAPA INTERNA (Dominio)
   ├── entities/              ← Entidades de negocio
   ├── ports/                 ← Puertos (Interfaces)
   └── use_cases/             ← Casos de uso

📁 infrastructure/            ← CAPA EXTERNA (Infraestructura)
   ├── database/              ← Detalles técnicos de BD
   └── repositories/          ← Adaptadores

📁 api/                       ← CAPA EXTERNA (Adaptador de Entrada)
   ├── routes.py              ← Endpoints REST
   ├── schemas.py             ← DTOs (Pydantic)
   └── dependencies.py        ← Dependency Injection
```

**Evidencia:**
- ✅ `domain/` contiene solo lógica de negocio pura
- ✅ `infrastructure/` contiene implementaciones técnicas
- ✅ `api/` contiene adaptadores HTTP
- ✅ Separación clara y sin dependencias cruzadas

#### 1.2 Implementar adaptadores para base de datos y API

**✅ CUMPLIDO**

**Adaptador de Base de Datos:**
- `infrastructure/repositories/ticket_repository.py` - Implementa `ITicketRepository` usando SQLAlchemy

**Adaptador de API:**
- `api/routes.py` - Transforma HTTP requests en llamadas al dominio

#### 1.3 Explicar el flujo de datos entre puertos y adaptadores

**✅ CUMPLIDO** - Ver sección [Flujo de Datos](#5-flujo-de-datos)

### ✅ 2. Uso del patrón Dependency Injection

#### 2.1 Implementar inyección de dependencias para mejorar el acoplamiento

**✅ CUMPLIDO**

**Implementación:**
- `api/dependencies.py` - Define funciones de inyección
- `api/routes.py` - Usa `Depends()` para inyectar dependencias
- Casos de uso reciben interfaces, no implementaciones

**Evidencia:**
- ✅ Dependencias inyectadas en constructores
- ✅ Uso de interfaces, no implementaciones concretas
- ✅ Acoplamiento reducido

#### 2.2 Justificar cómo el patrón mejora la mantenibilidad del sistema

**✅ CUMPLIDO** - Ver sección [Dependency Injection](#4-dependency-injection)

**Beneficios Demostrados:**
1. **Desacoplamiento**: Los casos de uso no conocen implementaciones concretas
2. **Testabilidad**: Fácil crear mocks para testing
3. **Flexibilidad**: Cambiar de MySQL a PostgreSQL: Solo cambiar adaptador
4. **Mantenibilidad**: Cambios en infraestructura no afectan dominio

### ✅ 3. Implementación Funcional

#### 3.1 CRUD completo de tickets

**✅ CUMPLIDO**

- **Create**: `POST /api/tickets/` → `CrearTicketUseCase`
- **Read**: `GET /api/tickets/` → `ListarTicketsUseCase`
- **Update**: `PUT /api/tickets/{id}` → `ActualizarEstadoTicketUseCase`
- **Delete**: `DELETE /api/tickets/{id}` → `EliminarTicketUseCase`

#### 3.2 Lógica desacoplada del acceso a datos

**✅ CUMPLIDO**

**Características:**
- ✅ No conoce SQL
- ✅ No conoce SQLAlchemy
- ✅ No conoce MySQL
- ✅ Solo usa interfaces (puertos)
- ✅ Lógica de negocio pura

#### 3.3 Validaciones y gestión de estados

**✅ CUMPLIDO**

**Validaciones implementadas en:**
- ✅ Entidades de dominio
- ✅ Casos de uso
- ✅ Schemas Pydantic

**Gestión de estados:**
- ✅ Transiciones validadas
- ✅ Reglas de negocio implementadas

### 📊 Resumen de Cumplimiento

| Requisito | Estado | Documentación |
|-----------|--------|---------------|
| **1. Arquitectura Hexagonal** | ✅ | Sección 2 |
| **1.1 Separación de capas** | ✅ | Sección 2.2 |
| **1.2 Adaptadores** | ✅ | Sección 2.4 |
| **1.3 Flujo de datos** | ✅ | Sección 5 |
| **2. Dependency Injection** | ✅ | Sección 4 |
| **2.1 Implementación** | ✅ | Sección 4.1 |
| **2.2 Justificación** | ✅ | Sección 4.2 |
| **3. Implementación Funcional** | ✅ | Sección 8 |
| **3.1 CRUD completo** | ✅ | Todos los endpoints implementados |
| **3.2 Lógica desacoplada** | ✅ | `domain/use_cases/` sin dependencias |
| **3.3 Validaciones** | ✅ | Múltiples capas de validación |

---

## 11. Guía de Uso

### 11.1 Ejemplos de Uso

#### Crear un ticket:
```bash
POST /api/tickets/
{
  "usuario_id": 1,
  "descripcion": "No puedo acceder a mi correo",
  "prioridad": "alta"
}
```

#### Asignar técnico:
```bash
POST /api/tickets/1/asignar-tecnico
{
  "tecnico_id": 2
}
```

#### Generar reporte por prioridad:
```bash
GET /api/tickets/reporte/prioridad/critica
```

### 11.2 Documentación API

- **Swagger UI**: `http://localhost:8888/docs`
- **ReDoc**: `http://localhost:8888/redoc`

### 11.3 Notas Importantes

- Asegúrate de crear primero algunos usuarios en la base de datos antes de crear tickets
- Los técnicos deben tener rol 'tecnico' o 'admin' en la tabla usuarios
- Los estados válidos son: `abierto`, `en_proceso`, `cerrado`
- Las prioridades válidas son: `baja`, `media`, `alta`, `critica`

---

## 12. Principios de Diseño

### 12.1 SOLID Principles

- **S**ingle Responsibility: Cada clase tiene una responsabilidad
- **O**pen/Closed: Abierto a extensión, cerrado a modificación
- **L**iskov Substitution: Interfaces pueden ser sustituidas
- **I**nterface Segregation: Interfaces específicas y pequeñas
- **D**ependency Inversion: Depender de abstracciones, no concreciones

### 12.2 Clean Architecture

- ✅ Reglas de dependencia: Capas externas dependen de internas
- ✅ Independencia de frameworks
- ✅ Independencia de UI
- ✅ Independencia de base de datos
- ✅ Independencia de agentes externos

---

## 📝 Conclusión

El sistema HelpDeskPro **CUMPLE COMPLETAMENTE** con todos los requisitos:

✅ Arquitectura Hexagonal implementada correctamente  
✅ Dependency Injection funcionando en todas las capas  
✅ CRUD completo de tickets y usuarios  
✅ Lógica completamente desacoplada del acceso a datos  
✅ Validaciones en múltiples capas  
✅ Gestión de estados con transiciones validadas  

**Todo el código está listo para producción y cumple con las mejores prácticas de arquitectura de software.**

---

**Última actualización:** 2024  
**Versión:** 1.0.0  
**Estado:** ✅ Completo y Documentado
