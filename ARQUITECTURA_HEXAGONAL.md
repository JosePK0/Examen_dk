# Arquitectura Hexagonal - HelpDeskPro

## Explicación del Flujo de Datos entre Puertos y Adaptadores

---

## 1. Conceptos Fundamentales

### ¿Qué es la Arquitectura Hexagonal?

La **Arquitectura Hexagonal** (también llamada **Ports & Adapters**) separa la aplicación en:
- **Núcleo (Domain)**: Lógica de negocio independiente
- **Periferia (Infrastructure/API)**: Detalles técnicos y adaptadores

### ¿Por qué se llama "Hexagonal"?

No significa que tenga 6 lados, sino que el hexágono representa que el dominio puede tener múltiples adaptadores (API REST, GraphQL, CLI, pruebas, etc.) sin cambiar el núcleo.

---

## 2. Separación de Capas en HelpDeskPro

### 2.1 Capa Interna (Dominio)

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

### 2.2 Capa Externa (Infraestructura)

```
infrastructure/
├── database/         # Configuración de BD y modelos ORM
└── repositories/     # Implementaciones de repositorios
```

**Características:**
- ✅ Implementa las interfaces del dominio
- ✅ Maneja detalles técnicos (SQLAlchemy, MySQL)
- ✅ Puede ser reemplazada sin afectar el dominio

### 2.3 Capa de Aplicación (API)

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

---

## 3. Puertos (Ports) - Las Interfaces

### 3.1 ¿Qué es un Puerto?

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

---

## 4. Adaptadores (Adapters) - Las Implementaciones

### 4.1 ¿Qué es un Adaptador?

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

---

## 5. Flujo de Datos Completo

### 5.1 Flujo: Cliente → API → Dominio → Infraestructura → BD

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

### 5.2 Flujo de Respuesta: BD → Infraestructura → Dominio → API → Cliente

```
Database (MySQL)
     │
     │ SELECT * FROM tickets WHERE IDticket = 1
     ▼
TicketRepository (Adaptador)
     │
     │ _to_entity(model) → Ticket Entity
     ▼
ITicketRepository (Puerto/Interface)
     │
     │ return ticket
     ▼
CrearTicketUseCase (Dominio)
     │
     │ return ticket
     ▼
routes.py (API)
     │
     │ TicketResponse.from_orm(ticket)
     ▼
Cliente (HTTP Response JSON)
```

---

## 6. Ejemplo Concreto: Asignar Técnico

### Paso a Paso

#### **Paso 1: Cliente envía request**
```http
POST /api/tickets/5/asignar-tecnico
Content-Type: application/json

{
  "tecnico_id": 10
}
```

#### **Paso 2: API recibe y valida**
```python
# api/routes.py
@router.post("/{ticket_id}/asignar-tecnico")
def asignar_tecnico(
    ticket_id: int,
    request: AsignarTecnicoRequest,  # ← Pydantic valida
    ticket_repo: ITicketRepository = Depends(get_ticket_repository),  # ← DI
    usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)  # ← DI
):
    # API NO conoce lógica de negocio
    # Solo orquesta las llamadas
```

#### **Paso 3: Dependency Injection**
```python
# api/dependencies.py
def get_ticket_repository(db: Session = Depends(get_db_session)) -> ITicketRepository:
    # ← Retorna la INTERFAZ, pero crea la IMPLEMENTACIÓN
    return TicketRepository(db)  # ← Adaptador SQLAlchemy
```

**¿Qué hace?**
- Crea una instancia de `TicketRepository` (adaptador)
- Pero la retorna como `ITicketRepository` (interfaz)
- El endpoint solo ve la interfaz, no la implementación

#### **Paso 4: Caso de Uso ejecuta lógica**
```python
# domain/use_cases/ticket_use_cases.py
class AsignarTecnicoUseCase:
    def __init__(self, ticket_repo: ITicketRepository, usuario_repo: IUsuarioRepository):
        # ← Recibe INTERFACES, no implementaciones
        self._ticket_repo = ticket_repo
        self._usuario_repo = usuario_repo
    
    def ejecutar(self, ticket_id: int, tecnico_id: int) -> Ticket:
        # 1. Obtener ticket usando el PUERTO
        ticket = self._ticket_repo.obtener_por_id(ticket_id)
        # ← No sabe si es SQLAlchemy, MongoDB, o archivo CSV
        
        # 2. Validar lógica de negocio
        if not ticket:
            raise ValueError("Ticket no existe")
        
        # 3. Obtener técnico usando el PUERTO
        tecnico = self._usuario_repo.obtener_por_id(tecnico_id)
        
        # 4. Validar reglas de negocio
        if not tecnico.es_tecnico():
            raise ValueError("No es técnico")
        
        # 5. Aplicar lógica de negocio en la ENTIDAD
        ticket.asignar_tecnico(tecnico_id)
        # ← La entidad maneja la transición de estado
        
        # 6. Guardar usando el PUERTO
        return self._ticket_repo.actualizar(ticket)
```

**Puntos clave:**
- ✅ El caso de uso **NO** conoce SQLAlchemy
- ✅ El caso de uso **NO** conoce MySQL
- ✅ Solo usa **interfaces** (puertos)
- ✅ La lógica de negocio está en la **entidad**

#### **Paso 5: Adaptador implementa persistencia**
```python
# infrastructure/repositories/ticket_repository.py
class TicketRepository(ITicketRepository):
    def __init__(self, session: Session):
        self._session = session  # ← SQLAlchemy Session
    
    def actualizar(self, ticket: Ticket) -> Ticket:
        # 1. Convertir Entidad → Modelo ORM
        model = self._to_model(ticket)
        
        # 2. Usar SQLAlchemy (detalle técnico)
        self._session.merge(model)
        self._session.commit()
        
        # 3. Convertir Modelo ORM → Entidad
        return self._to_entity(model)
```

**Puntos clave:**
- ✅ El adaptador **SÍ** conoce SQLAlchemy
- ✅ El adaptador **SÍ** conoce MySQL
- ✅ Puede ser reemplazado sin afectar el dominio

---

## 7. Ventajas de esta Arquitectura

### 7.1 Independencia del Dominio

**Escenario:** Cambiar de MySQL a PostgreSQL

**Con Arquitectura Hexagonal:**
```
✅ Solo cambia: infrastructure/repositories/ticket_repository.py
✅ NO cambia: domain/ (entidades, casos de uso, puertos)
✅ NO cambia: api/ (endpoints)
```

**Sin Arquitectura Hexagonal:**
```
❌ Cambia todo el código que accede a BD
❌ Cambia casos de uso
❌ Cambia entidades
❌ Cambia endpoints
```

### 7.2 Testabilidad

**Testing con Mocks:**
```python
# test_ticket_use_case.py
class MockTicketRepository(ITicketRepository):
    def crear(self, ticket):
        return ticket  # ← Simula BD sin usar BD real

def test_crear_ticket():
    mock_repo = MockTicketRepository()
    use_case = CrearTicketUseCase(mock_repo)
    ticket = use_case.ejecutar(1, "Problema", Prioridad.ALTA)
    assert ticket.descripcion == "Problema"
```

### 7.3 Flexibilidad

Puedes tener múltiples adaptadores:

```
ITicketRepository (Puerto)
    │
    ├──→ TicketRepository (SQLAlchemy) ← Producción
    ├──→ TicketRepositoryMock (Memoria) ← Testing
    └──→ TicketRepositoryFile (CSV) ← Desarrollo
```

El dominio **no sabe** cuál se está usando.

---

## 8. Reglas de Dependencia

### Regla de Oro de la Arquitectura Hexagonal

```
Las dependencias apuntan HACIA ADENTRO (hacia el dominio)

API → Domain ← Infrastructure
```

### Diagrama de Dependencias

```
┌─────────────┐
│     API     │
└──────┬──────┘
       │ depends on
       ▼
┌─────────────┐
│   Domain    │ ← Centro (NO depende de nadie)
└──────┬──────┘
       ▲
       │ implements
┌──────┴──────┐
│Infrastructure│
└─────────────┘
```

**Reglas:**
1. ✅ API depende de Domain
2. ✅ Infrastructure depende de Domain
3. ❌ Domain NO depende de API
4. ❌ Domain NO depende de Infrastructure
5. ❌ API NO depende directamente de Infrastructure

---

## 9. Resumen: Flujo de Datos

### Flujo Completo Simplificado

```
1. Cliente HTTP
   ↓
2. API Endpoint (Adaptador de Entrada)
   - Valida request
   - Inyecta dependencias
   ↓
3. Caso de Uso (Dominio)
   - Lógica de negocio
   - Valida reglas
   - Usa entidades
   ↓
4. Puerto (Interface)
   - Define contrato
   - No tiene implementación
   ↓
5. Adaptador (Infraestructura)
   - Implementa el puerto
   - Convierte Entidad ↔ Modelo ORM
   - Ejecuta SQL
   ↓
6. Base de Datos
   - Almacena datos
```

### Flujo de Respuesta

```
6. Base de Datos
   ↓
5. Adaptador
   - Modelo ORM → Entidad
   ↓
4. Puerto
   - Retorna entidad
   ↓
3. Caso de Uso
   - Retorna entidad
   ↓
2. API
   - Entidad → DTO (Pydantic)
   ↓
1. Cliente
   - Recibe JSON
```

---

## 10. Conclusión

### ✅ Cumplimiento de Requisitos

| Requisito | Estado | Ubicación |
|-----------|--------|-----------|
| **Separar capas internas/externas** | ✅ | `domain/` vs `infrastructure/` |
| **Implementar adaptadores** | ✅ | `infrastructure/repositories/` |
| **Puertos (interfaces)** | ✅ | `domain/ports/` |
| **Flujo de datos documentado** | ✅ | Este documento |

### Beneficios Logrados

1. ✅ **Mantenibilidad**: Cambios aislados por capa
2. ✅ **Testabilidad**: Fácil crear mocks
3. ✅ **Flexibilidad**: Cambiar tecnologías sin afectar dominio
4. ✅ **Escalabilidad**: Fácil agregar nuevos adaptadores
5. ✅ **Claridad**: Separación clara de responsabilidades

---

**El sistema HelpDeskPro implementa correctamente la Arquitectura Hexagonal con separación clara entre dominio e infraestructura, permitiendo que el núcleo de negocio sea independiente de los detalles técnicos.**

