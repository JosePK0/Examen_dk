"""
Script de ejemplo para demostrar el uso de la API HelpDeskPro
Este script muestra cómo interactuar con los endpoints
"""

import requests

BASE_URL = "http://localhost:8000/api"

# Ejemplo 1: Crear un ticket
def crear_ticket_ejemplo():
    """Ejemplo de creación de ticket"""
    url = f"{BASE_URL}/tickets/"
    data = {
        "usuario_id": 1,
        "descripcion": "No puedo acceder a mi correo electrónico",
        "prioridad": "alta"
    }
    response = requests.post(url, json=data)
    print("Crear ticket:", response.status_code)
    if response.status_code == 201:
        print("Ticket creado:", response.json())
    return response.json() if response.status_code == 201 else None

# Ejemplo 2: Listar todos los tickets
def listar_tickets_ejemplo():
    """Ejemplo de listado de tickets"""
    url = f"{BASE_URL}/tickets/"
    response = requests.get(url)
    print("\nListar tickets:", response.status_code)
    if response.status_code == 200:
        tickets = response.json()
        print(f"Total de tickets: {len(tickets)}")
        for ticket in tickets:
            print(f"  - Ticket {ticket['ticket_id']}: {ticket['descripcion'][:50]}...")
    return response.json() if response.status_code == 200 else None

# Ejemplo 3: Obtener un ticket por ID
def obtener_ticket_ejemplo(ticket_id: int):
    """Ejemplo de obtención de ticket por ID"""
    url = f"{BASE_URL}/tickets/{ticket_id}"
    response = requests.get(url)
    print(f"\nObtener ticket {ticket_id}:", response.status_code)
    if response.status_code == 200:
        print("Ticket:", response.json())
    return response.json() if response.status_code == 200 else None

# Ejemplo 4: Asignar técnico a un ticket
def asignar_tecnico_ejemplo(ticket_id: int, tecnico_id: int):
    """Ejemplo de asignación de técnico"""
    url = f"{BASE_URL}/tickets/{ticket_id}/asignar-tecnico"
    data = {"tecnico_id": tecnico_id}
    response = requests.post(url, json=data)
    print(f"\nAsignar técnico {tecnico_id} a ticket {ticket_id}:", response.status_code)
    if response.status_code == 200:
        print("Ticket actualizado:", response.json())
    return response.json() if response.status_code == 200 else None

# Ejemplo 5: Actualizar estado de un ticket
def actualizar_estado_ejemplo(ticket_id: int, nuevo_estado: str):
    """Ejemplo de actualización de estado"""
    url = f"{BASE_URL}/tickets/{ticket_id}"
    data = {"estado": nuevo_estado}
    response = requests.put(url, json=data)
    print(f"\nActualizar estado del ticket {ticket_id} a '{nuevo_estado}':", response.status_code)
    if response.status_code == 200:
        print("Ticket actualizado:", response.json())
    return response.json() if response.status_code == 200 else None

# Ejemplo 6: Generar reporte por prioridad
def reporte_prioridad_ejemplo(prioridad: str):
    """Ejemplo de reporte por prioridad"""
    url = f"{BASE_URL}/tickets/reporte/prioridad/{prioridad}"
    response = requests.get(url)
    print(f"\nReporte por prioridad '{prioridad}':", response.status_code)
    if response.status_code == 200:
        tickets = response.json()
        print(f"Total de tickets con prioridad {prioridad}: {len(tickets)}")
        for ticket in tickets:
            print(f"  - Ticket {ticket['ticket_id']}: {ticket['descripcion'][:50]}...")
    return response.json() if response.status_code == 200 else None

# Ejemplo 7: Generar reporte por estado
def reporte_estado_ejemplo(estado: str):
    """Ejemplo de reporte por estado"""
    url = f"{BASE_URL}/tickets/reporte/estado/{estado}"
    response = requests.get(url)
    print(f"\nReporte por estado '{estado}':", response.status_code)
    if response.status_code == 200:
        tickets = response.json()
        print(f"Total de tickets con estado {estado}: {len(tickets)}")
        for ticket in tickets:
            print(f"  - Ticket {ticket['ticket_id']}: {ticket['descripcion'][:50]}...")
    return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplos de uso de la API HelpDeskPro")
    print("=" * 60)
    print("\nNOTA: Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    print("      y que existan usuarios en la base de datos.\n")
    
    # Descomentar los ejemplos que quieras ejecutar:
    
    # crear_ticket_ejemplo()
    # listar_tickets_ejemplo()
    # obtener_ticket_ejemplo(1)
    # asignar_tecnico_ejemplo(1, 3)
    # actualizar_estado_ejemplo(1, "en_proceso")
    # reporte_prioridad_ejemplo("alta")
    # reporte_estado_ejemplo("abierto")

