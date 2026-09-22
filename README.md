# BarberPro — Sistema de cobros para barbería

Proyecto Django para la gestión de ventas y empleados de una barbería, con dos roles: **propietario** y **barbero**.

## Nota sobre los datos de prueba

En el modelo no existe una clase `BarberUser`: los barberos son usuarios del modelo `accounts.User` con `role='barber'`. Los nombres usados en datos de prueba para esos usuarios pueden variar y no tienen ningún significado especial.

---

## Stack

- Python / Django 6.x
- PostgreSQL en producción, SQLite por defecto en desarrollo local (según `DATABASE_URL`)
- `django-environ` para configuración por variables de entorno
- Bootstrap 5 + hoja de estilos propia (`static/css/theme.css`)
- `gunicorn` + `whitenoise` para despliegue en producción

---

## Funcionalidad

- Autenticación y redirección según rol (propietario / barbero)
- Panel del propietario: dashboard con métricas del día y la semana, listado de empleados, alta/edición/baja de empleados
- Panel del barbero: dashboard personal, perfil, registro y **edición** de sus propias ventas
- Modelos principales: `User`, `Client`, `Sale`
- Diseño responsive (sidebar del propietario colapsa a menú hamburguesa en móvil)

---

## Bugs corregidos

Estos problemas existían en versiones anteriores y ya están resueltos:

1. `Sale.__str__` usaba `self.barber` en vez de `self.user` (causaba `AttributeError`)
2. La ruta `/login` ejecutaba por error la vista de `logout`
3. Import incorrecto (`from tkinter import CASCADE`) en `reports/models.py`
4. Vistas de gestión de empleados sin `@login_required`
5. `owner_delete_employee` sin verificación de rol — cualquier usuario autenticado podía borrar empleados
6. `register_new_sale` sin `@login_required`
7. Conteo diario de cortes por barbero con bug de indentación (barberos sin ventas no aparecían)
8. `requirements.txt` guardado en UTF-16 (rompía `pip install` en Linux/CI)
9. Credenciales (usuario/contraseña) expuestas en consola por `print()` de debug
10. `db.sqlite3` estaba versionado en git a pesar del `.gitignore`
11. Vista de detalles de empleados comparaba un manager de Django contra un número (`barber.sales >= 50`), siempre evaluaba falso

---

## Seguridad y configuración

- `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` se leen desde variables de entorno (`.env`), nunca hardcodeadas
- Base de datos configurable vía `DATABASE_URL` (Postgres en producción, SQLite si no se define)
- Límite de contraseña corregido (antes `max_length=12`, ahora `min_length=8, max_length=128`)

---

## Pruebas

10 tests automatizados cubriendo login, logout, permisos por rol (propietario vs. barbero) y registro de ventas:

```
python manage.py test accounts sales
```

---

## Cómo arrancar en desarrollo

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / Mac

pip install -r requirements.txt
cp .env.example .env           # y completa tus propios valores
python manage.py migrate
python manage.py collectstatic
```

Para crear un usuario de prueba con rol (no uses `createsuperuser`, no permite elegir `role`):

```bash
python manage.py shell
```
```python
from accounts.models import User
User.objects.create_user(username='admin', password='tu_clave', role='owner', phone_number='000', first_name='Admin', last_name='Owner')
```

```bash
python manage.py runserver
```

---

## Variables de entorno (`.env`)

```
SECRET_KEY=una-clave-generada-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
```

Si no defines `DATABASE_URL`, el proyecto usa SQLite automáticamente.

---

## Despliegue

Preparado para desplegar en plataformas como Railway o Render:

- `Procfile` incluido (`web: gunicorn barbershop_system.wsgi --log-file -`)
- Archivos estáticos servidos por `whitenoise`
- Configuración 100% por variables de entorno

Pasos generales: conectar el repo, agregar una base Postgres, configurar `SECRET_KEY` / `DEBUG=False` / `ALLOWED_HOSTS` como variables en la plataforma, y correr `python manage.py migrate` desde la consola del servicio.

---

## Pendiente (mejoras futuras)

- CRUD completo de la app `clients`
- Implementar la app `reports` (actualmente registrada pero vacía)
- Internacionalización (`LANGUAGE_CODE` / `TIME_ZONE` en español/zona local)
- Corregir `RuntimeWarning` por comparación de fecha naive en `owner_dashboard`
