# Documentación Técnica - HelpDeskPro

## Sistema de Gestión de Incidencias

**Versión:** 1.0.0  
**Fecha:** 2024  
**Arquitectura:** Hexagonal (Ports & Adapters)  
**Framework:** FastAPI  
**Base de Datos:** MySQL

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Dependency Injection](#dependency-injection)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Flujo de Datos](#flujo-de-datos)
6. [Implementación Funcional](#implementación-funcional)
7. [Diagramas UML](#diagramas-uml)
8. [Guía de Uso](#guía-de-uso)

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

---

## 2. Arquitectura del Sistema

### 2.1 Arquitectura Hexagonal (Ports & Adapters)

La arquitectura hexagonal separa la aplicación en **capas internas (dominio)** y **capas externas (infraestructura)**, permitiendo que el dominio sea independiente de los detalles técnicos.

#### Capas del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE APLICACIÓN                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │         API (FastAPI) - Adaptador de Entrada     │   │
│  │  - routes.py (Tickets)                           │   │
│  │  - usuario_routes.py (Usuarios)                  │   │
│  │  - schemas.py (DTOs)                             │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE DOMINIO                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Entities (Entidades de Negocio)                 │   │
│  │  - Ticket                                         │   │
│  │  - Usuario                                        │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Ports (Interfaces) - Contratos                   │   │
│  │  - ITicketRepository                             │   │
│  │  - IUsuarioRepository                             │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Use Cases (Casos de Uso)                        │   │
│  │  - CrearTicketUseCase                            │   │
│  │  - AsignarTecnicoUseCase                         │   │
│  │  - ActualizarEstadoTicketUseCase                 │   │
│  │  - ...                                           │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  CAPA DE INFRAESTRUCTURA                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Adapters (Implementaciones)                      │   │
│  │  - TicketRepository (SQLAlchemy)                  │   │
│  │  - UsuarioRepository (SQLAlchemy)                 │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Database (Base de Datos)                        │   │
│  │  - models.py (ORM Models)                        │   │
│  │  - config.py (Conexión)                           │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Separación de Capas

#### **Capa Interna (Dominio)**
- **Entities**: Representan las entidades de negocio con su lógica
- **Ports**: Interfaces que definen contratos (repositorios)
- **Use Cases**: Contienen la lógica de negocio

#### **Capa Externa (Infraestructura)**
- **Adapters**: Implementaciones concretas de los puertos
- **Database**: Modelos ORM y configuración de BD
- **API**: Adaptadores de entrada (endpoints REST)

### 2.3 Ventajas de la Arquitectura Hexagonal

1. **Independencia del Dominio**: El dominio no depende de tecnologías externas
2. **Testabilidad**: Fácil de testear con mocks de los puertos
3. **Mantenibilidad**: Cambios en infraestructura no afectan el dominio
4. **Flexibilidad**: Cambiar de MySQL a PostgreSQL solo requiere cambiar adaptadores

---

## 3. Dependency Injection

### 3.1 Implementación

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

### 3.2 Beneficios del Dependency Injection

1. **Desacoplamiento**: Los casos de uso no conocen implementaciones concretas
2. **Testabilidad**: Fácil inyectar mocks en tests
3. **Flexibilidad**: Cambiar implementaciones sin modificar código cliente
4. **Mantenibilidad**: Código más limpio y organizado

### 3.3 Ejemplo de Inyección

```python
# Caso de uso recibe interfaz, no implementación
class CrearTicketUseCase:
    def __init__(self, ticket_repo: ITicketRepository, usuario_repo: IUsuarioRepository):
        self._ticket_repo = ticket_repo  # ← Dependencia inyectada
        self._usuario_repo = usuario_repo  # ← Dependencia inyectada
```

---

## 4. Estructura del Proyecto

```
Examen_dk/
├── api/                          # Capa de Aplicación (Adaptador de Entrada)
│   ├── dependencies.py          # Inyección de dependencias
│   ├── routes.py                # Endpoints de tickets
│   ├── usuario_routes.py       # Endpoints de usuarios
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
└── database_init.sql            # Script de inicialización
```

---

## 5. Flujo de Datos

### 5.1 Flujo de Creación de Ticket

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

### 5.2 Flujo de Asignación de Técnico

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

## 6. Implementación Funcional

### 6.1 CRUD Completo de Tickets

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

### 6.2 CRUD Completo de Usuarios

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

### 6.3 Lógica Desacoplada del Acceso a Datos

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

### 6.4 Validaciones y Gestión de Estados

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

#### Transiciones de Estado

```
ABIERTO → EN_PROCESO (al asignar técnico)
ABIERTO → CERRADO (❌ NO permitido)
EN_PROCESO → CERRADO (✅ Permitido)
CERRADO → (❌ No se pueden hacer cambios)
```

---

## 7. Diagramas UML

### 7.1 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer                            │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │   routes.py  │  │usuario_routes│                    │
│  └──────┬───────┘  └──────┬───────┘                    │
│         │                  │                            │
│         └──────────┬───────┘                            │
│                   ▼                                     │
│         ┌──────────────────┐                           │
│         │  dependencies.py │                           │
│         └──────────┬───────┘                           │
└────────────────────┼───────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Domain Layer                             │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │  Use Cases      │  │    Entities      │              │
│  │  - CrearTicket  │  │  - Ticket        │              │
│  │  - AsignarTecnico│  │  - Usuario       │              │
│  └────────┬────────┘  └────────┬─────────┘              │
│           │                    │                         │
│           └──────────┬──────────┘                         │
│                    ▼                                     │
│         ┌──────────────────────┐                         │
│         │      Ports           │                         │
│         │  ITicketRepository   │                         │
│         │  IUsuarioRepository  │                         │
│         └──────────┬───────────┘                         │
└────────────────────┼─────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Infrastructure Layer                          │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │  Repositories    │  │    Database      │              │
│  │  TicketRepository│  │  - models.py     │              │
│  │  UsuarioRepository│ │  - config.py     │              │
│  └────────┬─────────┘  └────────┬─────────┘              │
│           │                     │                        │
│           └──────────┬──────────┘                        │
│                     ▼                                    │
│              ┌─────────────┐                            │
│              │   MySQL      │                            │
│              └─────────────┘                            │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Diagrama de Clases - Entidades

```
┌─────────────────────────────────┐
│         Ticket (Entity)          │
├─────────────────────────────────┤
│ - ticket_id: int                 │
│ - usuario_id: int                │
│ - tecnico_id: Optional[int]      │
│ - descripcion: str               │
│ - prioridad: Prioridad           │
│ - estado: Estado                 │
│ - created_at: datetime           │
│ - updated_at: datetime           │
├─────────────────────────────────┤
│ + asignar_tecnico()              │
│ + actualizar_estado()             │
│ + actualizar_prioridad()         │
│ + actualizar_descripcion()       │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        Usuario (Entity)          │
├─────────────────────────────────┤
│ - usuario_id: int                │
│ - nombre: str                     │
│ - correo: str                     │
│ - contrasena: str                 │
│ - rol: Rol                        │
│ - activo: bool                    │
│ - created_at: datetime            │
│ - updated_at: datetime            │
├─────────────────────────────────┤
│ + es_tecnico() -> bool           │
│ + es_admin() -> bool             │
│ + es_usuario() -> bool           │
└─────────────────────────────────┘
```

### 7.3 Diagrama de Clases - Repositorios

```
┌─────────────────────────────────────┐
│      ITicketRepository (Port)       │
│         <<interface>>               │
├─────────────────────────────────────┤
│ + crear(ticket) -> Ticket           │
│ + obtener_por_id(id) -> Ticket     │
│ + obtener_todos() -> List[Ticket]   │
│ + actualizar(ticket) -> Ticket      │
│ + eliminar(id) -> bool              │
│ + obtener_por_prioridad()           │
│ + obtener_por_estado()              │
└─────────────────────────────────────┘
                  ▲
                  │ implements
                  │
┌─────────────────────────────────────┐
│   TicketRepository (Adapter)        │
├─────────────────────────────────────┤
│ - _session: Session                 │
├─────────────────────────────────────┤
│ + crear(ticket) -> Ticket           │
│ + obtener_por_id(id) -> Ticket     │
│ + obtener_todos() -> List[Ticket]   │
│ + actualizar(ticket) -> Ticket      │
│ + eliminar(id) -> bool              │
│ - _to_entity(model) -> Ticket       │
│ - _to_model(entity) -> TicketModel  │
└─────────────────────────────────────┘
```

### 7.4 Diagrama de Secuencia - Crear Ticket

```
Cliente          API          Use Case        Repository      Database
  │              │              │                │              │
  │──POST /api/──>│              │                │              │
  │  tickets/     │              │                │              │
  │              │              │                │              │
  │              │──Dependency──>│                │              │
  │              │  Injection    │                │              │
  │              │              │                │              │
  │              │──ejecutar()──>│                │              │
  │              │              │                │              │
  │              │              │──obtener_por──>│              │
  │              │              │    _id()       │              │
  │              │              │                │──SELECT──>    │
  │              │              │                │<──Usuario──   │
  │              │              │<──Usuario──────│              │
  │              │              │                │              │
  │              │              │──crear()──────>│              │
  │              │              │                │              │
  │              │              │                │──_to_model() │
  │              │              │                │──INSERT──>    │
  │              │              │                │              │
  │              │              │                │<──TicketModel │
  │              │              │<──Ticket────────│              │
  │              │<──Ticket─────│                │              │
  │<──Response───│              │                │              │
```

### 7.5 Diagrama de Secuencia - Asignar Técnico

```
Cliente          API          Use Case        TicketRepo    UsuarioRepo    Database
  │              │              │                │              │              │
  │──POST──>      │              │                │              │              │
  │  /asignar-    │              │                │              │              │
  │  tecnico       │              │                │              │              │
  │              │              │                │              │              │
  │              │──ejecutar()──>│                │              │              │
  │              │              │                │              │              │
  │              │              │──obtener_por──>│              │              │
  │              │              │    _id()       │              │              │
  │              │              │                │──SELECT──>    │              │
  │              │              │                │<──Ticket──    │              │
  │              │              │<──Ticket───────│              │              │
  │              │              │                │              │              │
  │              │              │──obtener_por──>│              │              │
  │              │              │    _id()       │              │              │
  │              │              │                │              │──SELECT──>    │
  │              │              │                │              │<──Usuario──   │
  │              │              │<──Usuario──────│              │              │
  │              │              │                │              │              │
  │              │              │──asignar_───>  │              │              │
  │              │              │   tecnico()    │              │              │
  │              │              │                │              │              │
  │              │              │──actualizar()─>│              │              │
  │              │              │                │──UPDATE──>   │              │
  │              │              │                │<──Ticket──    │              │
  │              │              │<──Ticket───────│              │              │
  │              │<──Ticket─────│                │              │              │
  │<──Response───│              │                │              │              │
```

---

## 8. Guía de Uso

### 8.1 Instalación

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp config.env.example .env
# Editar .env con tus credenciales

# 3. Inicializar base de datos
mysql -u root -p < database_init.sql

# 4. Ejecutar aplicación
python main.py
```

### 8.2 Endpoints Principales

#### Tickets
- `POST /api/tickets/` - Crear ticket
- `GET /api/tickets/` - Listar todos
- `GET /api/tickets/{id}` - Obtener por ID
- `PUT /api/tickets/{id}` - Actualizar ticket
- `DELETE /api/tickets/{id}` - Eliminar ticket
- `POST /api/tickets/{id}/asignar-tecnico` - Asignar técnico

#### Usuarios
- `POST /api/usuarios/` - Crear usuario
- `GET /api/usuarios/` - Listar todos
- `GET /api/usuarios/{id}` - Obtener por ID
- `PUT /api/usuarios/{id}` - Actualizar usuario
- `DELETE /api/usuarios/{id}` - Eliminar usuario
- `GET /api/usuarios/tecnicos/list` - Listar técnicos

### 8.3 Documentación API

- Swagger UI: `http://localhost:8888/docs`
- ReDoc: `http://localhost:8888/redoc`

---

## 9. Principios de Diseño Aplicados

### 9.1 SOLID Principles

- **S**ingle Responsibility: Cada clase tiene una responsabilidad
- **O**pen/Closed: Abierto a extensión, cerrado a modificación
- **L**iskov Substitution: Interfaces pueden ser sustituidas
- **I**nterface Segregation: Interfaces específicas y pequeñas
- **D**ependency Inversion: Depender de abstracciones, no concreciones

### 9.2 Clean Architecture

- ✅ Reglas de dependencia: Capas externas dependen de internas
- ✅ Independencia de frameworks
- ✅ Independencia de UI
- ✅ Independencia de base de datos
- ✅ Independencia de agentes externos

---

## 10. Conclusiones

El sistema HelpDeskPro cumple con todos los requisitos:

✅ **Arquitectura Hexagonal**: Separación clara entre dominio e infraestructura  
✅ **Dependency Injection**: Implementado con FastAPI Depends  
✅ **CRUD Completo**: Todas las operaciones implementadas  
✅ **Lógica Desacoplada**: Casos de uso independientes de BD  
✅ **Validaciones**: Implementadas en múltiples capas  
✅ **Gestión de Estados**: Transiciones validadas en entidades

El diseño permite fácil mantenimiento, testing y extensibilidad futura.

