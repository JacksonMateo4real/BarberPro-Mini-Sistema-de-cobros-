# Sistema de cobros (barbería)

Proyecto Django para registro de ventas de servicios (cortes, barba, etc.), con roles **propietario** y **barbero**.

## Nota sobre los nombres de los barberos

En el modelo no hay una clase llamada `BarberUser`: los barberos son usuarios del modelo `accounts.User` con `role='barber'`. **Los nombres que se usan para esos usuarios barbero (BarberUser a nivel de negocio / datos de prueba) son nombres de peloteros**, solo como convención temática para desarrollo y demostración.

---

## Lo que ya está

- Autenticación y redirección según rol (propietario / barbero).
- Panel del propietario: dashboard con métricas básicas, listado de empleados, alta de empleado barbero.
- Panel del barbero: dashboard, perfil, registro de ventas (`sales`) vinculado al usuario y al cliente.
- Modelos principales: `User`, `Client`, `Sale`; app `reports` registrada pero sin lógica útil aún.

---

## Lo que falta para considerar el proyecto terminado

### Funcionalidad

1. **Gestión de empleados (propietario)**  
   - `owner_update_employee_view` y `owner_update_employee` están sin implementar (`pass`).  
   - `owner_delete_employee` tiene errores (por ejemplo referencias incorrectas al request y a `POST`) y debe completarse y alinear con las URLs (`<int:id>` vs parámetros en la vista).

2. **Perfil del propietario**  
   - Revisar la consulta de usuario en `owner_profile` (filtro por `id` respecto a `request.user`).

3. **App `clients`**  
   - No hay vistas ni rutas públicas: falta CRUD o al menos listado/edición de clientes si el negocio lo requiere.

4. **App `reports`**  
   - El modelo `Report` está vacío; no hay vistas ni URLs. Definir qué reportes se necesitan (por fechas, por barbero, totales, exportación, etc.) e implementarlos.

5. **Ventas**  
   - Proteger con `@login_required` (y permisos de rol si aplica) la vista de registro de ventas para que solo usuarios autenticados la usen de forma coherente con el resto del sitio.

6. **Modelo `Sale`**  
   - En `__str__` se usa `self.barber`, pero el campo definido es `user`; conviene corregirlo para evitar errores al mostrar el objeto.

### Calidad y despliegue

7. **Pruebas**  
   - Los `tests.py` de las apps están casi vacíos; añadir pruebas mínimas de flujos críticos (login, registro de venta, permisos por rol).

8. **Producción**  
   - `SECRET_KEY` fija en código, `DEBUG=True`, `ALLOWED_HOSTS` vacío: documentar o aplicar configuración por variables de entorno antes de desplegar.

9. **Internacionalización**  
   - `LANGUAGE_CODE` y `TIME_ZONE` están en inglés/UTC; valorar español y zona horaria local si el producto es para uso regional.

10. **Rutas y UX**  
    - Revisar nombres de rutas (por ejemplo la ruta asociada al cierre de sesión) para que sean claras y consistentes.

---

## Cómo arrancar (desarrollo)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ajusta los pasos según tu entorno (por ejemplo activación del venv en PowerShell).

---

## Stack

- Python / Django 6.x  
- SQLite (por defecto en `settings.py`)
