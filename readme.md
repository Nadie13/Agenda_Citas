# Agenda de Citas — JES Beauty Studio 

Sistema web para gestionar citas de un estudio de belleza. Permite registrarse,
iniciar sesión, consultar servicios y administrar citas, horarios y perfiles de
usuario según su rol (`administrador`, `gestor` o `clientes`).

Está construido con **Django + PostgreSQL** en el backend, **React/Vite** en el
frontend, y se ejecuta con **Docker Compose** (Gunicorn + Nginx).

---

## 1. Metodología: Modelo en V (fase descendente)

### ¿Qué es el modelo en V?

El **modelo en V** es una metodología de desarrollo de software en la que el
trabajo se organiza en dos ramas que forman una "V":

- **Rama descendente (izquierda):** se analiza, se diseña y se construye el sistema.
- **Parte inferior:** la implementación o codificación.
- **Rama ascendente (derecha):** se prueba y se valida cada etapa.

La característica principal es que **cada fase de la rama descendente tiene una
prueba equivalente en la rama ascendente**. Así, los requisitos se validan con
pruebas de aceptación, el diseño con pruebas de integración y el diseño detallado
con pruebas unitarias.

### Fases de la rama descendente

| Fase | ¿En qué consiste? | Entregables típicos |
|------|-------------------|---------------------|
| **1. Análisis de requisitos** | Se identifican las necesidades del cliente y se define qué debe hacer el sistema. | Documento de requisitos funcionales y no funcionales, casos de uso, alcance. |
| **2. Diseño del sistema** | Se define la arquitectura general, las tecnologías y la comunicación entre componentes. | Diagrama de arquitectura, elección de tecnologías, diseño de la base de datos. |
| **3. Diseño detallado** | Se especifican módulos, clases, tablas, interfaces y pantallas. | Diagramas de clases y de base de datos, diseño de interfaces, contratos de la API. |
| **4. Implementación** | Se escribe el código siguiendo los diseños anteriores y se prepara el despliegue. | Código fuente, pruebas básicas, scripts de despliegue, manual técnico. |

> **Nota:** la **rama ascendente** (pruebas unitarias, de integración, del
> sistema y de aceptación) corresponde a la verificación del software y se
> ejecuta después de cada fase descendente. Este documento explica únicamente la
> rama descendente de forma sencilla.

---

## 2. Tecnologías utilizadas

- **Backend:** Django 6, PostgreSQL 17, Gunicorn.
- **Frontend:** React 19 + Vite.
- **Servidor web / proxy:** Nginx.
- **Contenedores:** Docker y Docker Compose.
- **Librerías destacadas:** `django-crispy-forms`, `crispy-bootstrap5`, `psycopg2-binary`, `python-dotenv`, `Pillow`.

---

## 3. Requisitos previos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/) (incluido en Docker Desktop)
- Puertos libres: **80** (Nginx), **3000** (frontend) y **5433** (PostgreSQL).

No necesitas instalar Python ni Node si vas a usar Docker.

---

## 4. Cómo ejecutar el proyecto

### Paso 1: Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd "AGENDA CITAS"
```

### Paso 2: Configurar las variables de entorno

El repositorio **no incluye el archivo `.env`** (por seguridad no se sube). Usa
`.env.example` como plantilla para crear el tuyo:

```bash
cp .env.example .env
```

Luego edita `.env` y ajusta los valores:

```env
DJANGO_SECRET_KEY="cambia-esta-clave-por-una-segura"
DEBUG=True
DJANGO_ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1

DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=bd_agenda_de_citas
DATABASE_USERNAME=appuser
DATABASE_PASSWORD=cambia-esta-contrasena
DATABASE_HOST=localhost
DATABASE_PORT=5433
```

> **Importante:** `DATABASE_HOST` y `DATABASE_PORT` del `.env` son para ejecutar
> Django **fuera** de Docker. Dentro de Docker, `compose.yaml` los sobrescribe
> con `db` y `5432`, porque así se llama el servicio de PostgreSQL en la red de
> contenedores.

También puedes cambiar las credenciales de los usuarios iniciales:

```env
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=cambia-esta-contrasena
GESTOR_USERNAME=gestor
GESTOR_EMAIL=gestor@example.com
GESTOR_PASSWORD=cambia-esta-contrasena
```

> Si cambias `DATABASE_USERNAME` o `DATABASE_PASSWORD` antes del primer arranque,
> PostgreSQL creará el usuario con esos valores automáticamente. Si la base de
> datos ya existe, tendrás que actualizar la contraseña o borrar el volumen con
> `docker compose down -v` (esto elimina los datos).

### Paso 3: Levantar los contenedores

```bash
docker compose up --build
```

O en segundo plano:

```bash
docker compose up --build -d
```

Al arrancar, el contenedor de Django ejecuta automáticamente:

1. `collectstatic` — reúne los archivos estáticos.
2. `migrate` — crea/actualiza las tablas en PostgreSQL.
3. `create_initial_users` — crea los usuarios iniciales (si no existen).
4. Gunicorn — inicia el servidor de la aplicación.

### Paso 4: Abrir la aplicación

| Servicio | URL |
|----------|-----|
| Aplicación (Django vía Nginx) | <http://localhost> |
| Panel de administración | <http://localhost/admin/> |
| Frontend (React/Vite) | <http://localhost:3000> |

### Usuarios creados automáticamente

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | La definida en `DJANGO_SUPERUSER_PASSWORD` | Superusuario + grupo `administrador` |
| `gestor` | La definida en `GESTOR_PASSWORD` | Grupo `gestor` |

> Las credenciales se toman del `.env`. Cámbialas antes de usar el proyecto en
> producción. Los usuarios también se pueden crear manualmente desde `/register/`.

---

## 5. Comandos útiles

```bash
# Ver los logs del backend en tiempo real
docker compose logs -f django-web

# Detener los contenedores (conserva la base de datos)
docker compose down

# Detener y borrar también la base de datos (¡se pierden los datos!)
docker compose down -v

# Aplicar migraciones manualmente
docker compose exec django-web python manage.py migrate

# Crear los usuarios iniciales de nuevo (idempotente)
docker compose exec django-web python manage.py create_initial_users

# Crear otro superusuario manualmente
docker compose exec django-web python manage.py createsuperuser

# Reconstruir después de cambiar código del backend
docker compose up -d --build django-web
```

---

## 6. Ejecución sin Docker (opcional, para desarrollo)

### Backend

```bash
cd BACKEND
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# Necesitas PostgreSQL escuchando en localhost:5433 (según tu .env)
python manage.py migrate
python manage.py create_initial_users
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 7. Estructura del proyecto

```text
AGENDA CITAS/
├── compose.yaml              # Servicios: db, django-web, nginx, frontend
├── nginx.conf                # Proxy de Nginx hacia Gunicorn y estáticos
├── .env.example              # Plantilla de variables de entorno
├── .env                      # Tu configuración local (NO se sube al repositorio)
├── .gitignore                # Excluye .env, venv, node_modules, etc.
├── BACKEND/
│   ├── agenda/               # Configuración del proyecto Django
│   ├── accounts/             # Perfiles de usuario y roles
│   ├── bd/                   # Modelos de servicios, citas y horarios
│   ├── core/                 # Vistas, formularios, plantillas y usuarios iniciales
│   ├── entrypoint.sh         # Migraciones + usuarios iniciales + Gunicorn
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/                 # Aplicación React + Vite
```

---

## 8. Rutas principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página de inicio |
| `/register/` | Registro de nuevos usuarios |
| `/accounts/login/` | Inicio de sesión |
| `/services/` | Catálogo de servicios (requiere sesión) |
| `/config/` | Panel de configuración (solo grupo `gestor`) |
| `/admin/` | Administración de Django |
| `/logout` | Cerrar sesión (solo método POST) |

---


