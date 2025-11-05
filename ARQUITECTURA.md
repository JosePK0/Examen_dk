# Arquitectura Hexagonal - HelpDeskPro

## 📐 Descripción de la Arquitectura

Este proyecto implementa la **Arquitectura Hexagonal (Ports & Adapters)**, también conocida como arquitectura de puertos y adaptadores. Esta arquitectura separa la lógica de negocio (dominio) de los detalles de implementación (infraestructura y API).

## 🏛️ Capas de la Arquitectura

### 1. **Dominio (Capa Interna - Núcleo)**

El dominio es la capa más interna y contiene:

#### Entidades (`domain/entities/`)
- **Ticket**: Entidad de dominio que representa un ticket con toda su lógica de negocio
- **Usuario**: Entidad de dominio que representa un usuario del sistema

**Características:**
- Contienen lógica de negocio (métodos como `asignar_tecnico()`, `actualizar_estado()`)
- No dependen de ninguna tecnología externa
- Son agnósticas a la base de datos

#### Puertos (`domain/ports/`)
- **ITicketRepository**: Interfaz que define las operaciones posibles sobre tickets
- **IUsuarioRepository**: Interfaz que define las operaciones posibles sobre usuarios

**Características:**
- Son **interfaces** (contratos)
- Definen QUÉ se puede hacer, no CÓMO
- El dominio depende de estos puertos, no de implementaciones concretas

#### Casos de Uso (`domain/use_cases/`)
- **CrearTicketUseCase**: Lógica para crear un ticket
- **AsignarTecnicoUseCase**: Lógica para asignar un técnico
- **GenerarReportePorPrioridadUseCase**: Lógica para generar reportes
- Y otros casos de uso...

**Características:**
- Contienen la lógica de aplicación
- Orquestan las operaciones de las entidades
- Dependen de los puertos (interfaces), no de implementaciones

### 2. **Infraestructura (Adaptadores de Salida)**

La infraestructura implementa los puertos definidos en el dominio:

#### Repositorios (`infrastructure/repositories/`)
- **TicketRepository**: Implementa `ITicketRepository` usando SQLAlchemy
- **UsuarioRepository**: Implementa `IUsuarioRepository` usando SQLAlchemy

**Características:**
- Son **adaptadores** que conectan el dominio con la base de datos
- Implementan las interfaces definidas en los puertos
- Pueden cambiar sin afectar el dominio (podríamos cambiar a MongoDB, PostgreSQL, etc.)

#### Modelos de Base de Datos (`infrastructure/database/models.py`)
- **TicketModel**: Modelo SQLAlchemy que mapea la tabla `tickets`
- **UsuarioModel**: Modelo SQLAlchemy que mapea la tabla `usuarios`

**Características:**
- Representan la estructura de la base de datos
- Se convierten a/desde entidades de dominio en los repositorios

### 3. **API (Adaptadores de Entrada)**

La API es el punto de entrada de la aplicación:

#### Endpoints (`api/routes.py`)
- Endpoints REST para todas las operaciones CRUD
- Reciben peticiones HTTP y las convierten en llamadas a casos de uso

#### Schemas (`api/schemas.py`)
- **TicketCreate**, **TicketResponse**, etc.
- Validan los datos de entrada y formatean las respuestas

#### Dependency Injection (`api/dependencies.py`)
- Funciones que proveen las dependencias necesarias
- FastAPI usa estas funciones para inyectar automáticamente los repositorios y casos de uso

## 🔄 Flujo de Datos

### Ejemplo: Crear un Ticket

```
1. Cliente HTTP → POST /api/tickets/
   ↓
2. FastAPI (routes.py) → valida schema (TicketCreate)
   ↓
3. Dependency Injection → inyecta repositorios y casos de uso
   ↓
4. CrearTicketUseCase → ejecuta lógica de negocio
   ↓ (usa interfaz ITicketRepository)
5. TicketRepository (implementación) → convierte entidad a modelo
   ↓
6. SQLAlchemy → ejecuta INSERT en MySQL
   ↓
7. Respuesta fluye de vuelta → TicketResponse → JSON → Cliente
```

### Separación de Responsabilidades

- **API**: Solo se encarga de HTTP (recibir requests, validar, responder)
- **Casos de Uso**: Orquestan la lógica de negocio
- **Entidades**: Contienen las reglas de negocio
- **Repositorios**: Solo se encargan de persistencia
- **Modelos DB**: Solo representan la estructura de BD

## 🔌 Dependency Injection

### ¿Qué es?

La **Inyección de Dependencias (DI)** es un patrón donde las dependencias se "inyectan" en lugar de crearse internamente.

### Ejemplo sin DI (acoplado):

```python
class CrearTicketUseCase:
    def __init__(self):
        # ❌ Crea la dependencia internamente
        self._repo = TicketRepository(SessionLocal())
```

### Ejemplo con DI (desacoplado):

```python
class CrearTicketUseCase:
    def __init__(self, ticket_repo: ITicketRepository):
        # ✅ La dependencia se inyecta desde fuera
        self._ticket_repo = ticket_repo

# En FastAPI:
@router.post("/")
def crear_ticket(
    ticket_repo: ITicketRepository = Depends(get_ticket_repository)
):
    # FastAPI inyecta automáticamente el repositorio
    use_case = CrearTicketUseCase(ticket_repo)
```

### Ventajas de DI:

1. **Testing**: Fácil crear mocks para tests
2. **Mantenibilidad**: Cambiar implementaciones es fácil
3. **Desacoplamiento**: El código no depende de implementaciones concretas
4. **Flexibilidad**: Puedes cambiar de MySQL a PostgreSQL sin tocar el dominio

## 📊 Diagrama de Dependencias

```
┌─────────────────────────────────────────┐
│         API (FastAPI Routes)            │
│  - Recibe HTTP requests                 │
│  - Valida con Pydantic                  │
└──────────────┬──────────────────────────┘
               │ usa
               ↓
┌─────────────────────────────────────────┐
│      Casos de Uso (Use Cases)           │
│  - Orquestan lógica de negocio          │
│  - Validan reglas de negocio            │
└──────────────┬──────────────────────────┘
               │ usa (interfaces)
               ↓
┌─────────────────────────────────────────┐
│      Puertos (Interfaces)               │
│  - ITicketRepository                    │
│  - IUsuarioRepository                   │
└──────────────┬──────────────────────────┘
               │ implementado por
               ↓
┌─────────────────────────────────────────┐
│   Repositorios (Implementaciones)       │
│  - TicketRepository (SQLAlchemy)        │
│  - UsuarioRepository (SQLAlchemy)       │
└──────────────┬──────────────────────────┘
               │ usa
               ↓
┌─────────────────────────────────────────┐
│      Base de Datos (MySQL)              │
└─────────────────────────────────────────┘
```

## 🎯 Principios Aplicados

### 1. **Separación de Responsabilidades (SRP)**
   - Cada clase tiene una única responsabilidad
   - Las entidades solo contienen lógica de negocio
   - Los repositorios solo se encargan de persistencia

### 2. **Inversión de Dependencias (DIP)**
   - El dominio depende de abstracciones (puertos), no de implementaciones
   - Los adaptadores dependen del dominio, no al revés

### 3. **Abierto/Cerrado (OCP)**
   - Abierto para extensión (nuevos repositorios, nuevos casos de uso)
   - Cerrado para modificación (no necesitas cambiar el dominio)

### 4. **Dependency Inversion**
   - Las dependencias se inyectan, no se crean internamente
   - Facilita el testing y el cambio de implementaciones

## 🧪 Facilidad para Testing

Gracias a la arquitectura hexagonal y DI, es muy fácil hacer tests:

```python
# Mock del repositorio
class MockTicketRepository(ITicketRepository):
    def crear(self, ticket):
        return ticket

# Test sin necesidad de base de datos
def test_crear_ticket():
    mock_repo = MockTicketRepository()
    use_case = CrearTicketUseCase(mock_repo)
    ticket = use_case.ejecutar(...)
    assert ticket is not None
```

## 📝 Resumen

1. **Dominio**: Contiene la lógica de negocio pura, sin dependencias externas
2. **Puertos**: Interfaces que definen contratos
3. **Adaptadores**: Implementan los puertos (repositorios, API)
4. **DI**: Inyecta dependencias para desacoplar componentes
5. **Resultado**: Sistema mantenible, testeable y flexible

