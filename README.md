# ProF4 - Sistema Integral de Gestión de Clientes, Servicios y Reservas (Software FJ)

**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Programa:** Ingeniería de Sistemas — **Curso:** Programación (`213023`)  
**Fase 4:** Componente Práctico (Prácticas Simuladas)  

---

## Descripción del Proyecto
Aplicación modular desarrollada en Python bajo el paradigma de **Programación Orientada a Objetos (POO)** para la empresa **Software FJ**. Gestiona en memoria (mediante listas y objetos, sin bases de datos) clientes, servicios especializados y reservas, incorporando manejo avanzado de excepciones y auditoría en archivos de logs.

## Estructura del Proyecto
* `software_fj/entidad.py`: Clase abstracta base `Entidad` (abstracción y encapsulación).
* `software_fj/cliente.py`: Clase `Cliente` con validaciones y propiedades `@property`.
* `software_fj/servicios.py`: Clase abstracta `Servicio` y subclases (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) con polimorfismo y sobrecarga.
* `software_fj/reserva.py`: Clase `Reserva` con control de estados (`pendiente`, `confirmada`, `cancelada`, `procesada`) y encadenamiento de excepciones.
* `software_fj/excepciones.py`: Excepciones personalizadas del sistema (`FJ-000` a `FJ-007`).
* `software_fj/logger.py`: Registro de eventos y errores en `logs/software_fj.log`.
* `software_fj/main.py`: Simulación integral con 12 operaciones completas (exitosas y fallidas).

## Ejecución
```bash
cd software_fj
python3 main.py