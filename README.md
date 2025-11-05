# HelpDeskPro - Sistema de Gestión de Incidencias

Sistema completo de gestión de tickets con arquitectura hexagonal (Ports & Adapters) implementado en FastAPI.

## 🏗️ Arquitectura

Este proyecto implementa la **Arquitectura Hexagonal (Ports & Adapters)**, que separa la lógica de negocio del acceso a datos y la interfaz de usuario.

### Estructura del Proyecto

```
Examen_dk/
├── domain/                    # Capa de Dominio (Núcleo)
│   ├── entities/             # Entidades de dominio
│   │   ├── ticket.py
│   │   └── usuario.py
│   ├── ports/                # Puertos (Interfaces)
│   │   ├── ticket_repository.py
│   │   └── usuario_repository.py
│   └── use_cases/            # Casos de uso
│       └── ticket_use_cases.py
├── infrastructure/           # Capa de Infraestructura (Adaptadores)
│   ├── database/
│   │   ├── config.py        # Configuración de BD
│   │   └── models.py        # Modelos SQLAlchemy
│   └── repositories/         # Implementaciones de repositorios
│       ├── ticket_repository.py
│       └── usuario_repository.py
├── api/                      # Capa de API (Adaptador)
│   ├── schemas.py           # Schemas Pydantic
│   ├── dependencies.py      # Dependency Injection
│   └── routes.py            # Endpoints FastAPI
├── main.py                   # Aplicación principal
├── requirements.txt
└── README.md
```

## 🔄 Flujo de Datos

```
API (routes.py)
    ↓ (Dependency Injection)
Casos de Uso (use_cases)
    ↓ (usa interfaces)
Puertos (ports) - Interfaces
    ↓ (implementado por)
Adaptadores (repositories)
    ↓ (accede a)
Base de Datos (MySQL)
```

## 📦 Instalación

1. **Clonar o navegar al proyecto:**
```bash
cd Examen_dk
```

2. **Crear un entorno virtual:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos:**
   - Crear la base de datos `helpdesk_db` en MySQL
   - Ejecutar los scripts SQL proporcionados para crear las tablas
   - Copiar `.env.example` a `.env` y configurar las credenciales

5. **Ejecutar la aplicación:**
```bash
python main.py
```

O con uvicorn directamente:
```bash
uvicorn main:app --reload
```

## 🚀 Endpoints Disponibles

### Tickets

- `POST /api/tickets/` - Crear un nuevo ticket
- `GET /api/tickets/` - Listar todos los tickets
- `GET /api/tickets/{ticket_id}` - Obtener un ticket por ID
- `PUT /api/tickets/{ticket_id}` - Actualizar un ticket
- `POST /api/tickets/{ticket_id}/asignar-tecnico` - Asignar técnico a un ticket
- `GET /api/tickets/reporte/prioridad/{prioridad}` - Reporte por prioridad
- `GET /api/tickets/reporte/estado/{estado}` - Reporte por estado
- `DELETE /api/tickets/{ticket_id}` - Eliminar un ticket

### Documentación

- `GET /docs` - Documentación interactiva (Swagger UI)
- `GET /redoc` - Documentación alternativa (ReDoc)

## 🔧 Dependency Injection

El sistema utiliza **Dependency Injection** para desacoplar las dependencias:

- Los repositorios se inyectan en los casos de uso
- Los casos de uso se inyectan en los endpoints
- Las sesiones de BD se gestionan automáticamente

**Ventajas:**
- ✅ Facilita el testing (mocks fáciles de crear)
- ✅ Mejora la mantenibilidad
- ✅ Reduce el acoplamiento entre componentes
- ✅ Permite cambiar implementaciones sin modificar el código de negocio

## 📋 Características Implementadas

### ✅ Arquitectura Hexagonal
- Separación clara entre dominio, infraestructura y API
- Puertos (interfaces) definen contratos
- Adaptadores implementan los puertos

### ✅ Dependency Injection
- Inyección de dependencias en todos los niveles
- Desacoplamiento completo

### ✅ CRUD Completo
- Crear, leer, actualizar y eliminar tickets
- Validaciones en el dominio
- Gestión de estados

### ✅ Lógica Desacoplada
- La lógica de negocio no depende de la BD
- Fácil cambiar de MySQL a PostgreSQL, MongoDB, etc.

### ✅ Validaciones
- Validaciones en entidades de dominio
- Validaciones en casos de uso
- Validaciones en schemas Pydantic

## 🎯 Ejemplos de Uso

### Crear un ticket:
```bash
POST /api/tickets/
{
  "usuario_id": 1,
  "descripcion": "No puedo acceder a mi correo",
  "prioridad": "alta"
}
```

### Asignar técnico:
```bash
POST /api/tickets/1/asignar-tecnico
{
  "tecnico_id": 2
}
```

### Generar reporte por prioridad:
```bash
GET /api/tickets/reporte/prioridad/critica
```

## 📝 Notas

- Asegúrate de crear primero algunos usuarios en la base de datos antes de crear tickets
- Los técnicos deben tener rol 'tecnico' o 'admin' en la tabla usuarios
- Los estados válidos son: abierto, en_proceso, cerrado
- Las prioridades válidas son: baja, media, alta, critica

