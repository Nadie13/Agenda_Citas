#!/bin/sh
set -e

# Asegura que el volumen montado pertenezca a appuser
chown -R appuser:appuser /app/staticfiles

# Ejecuta collectstatic como appuser
su-exec appuser python manage.py collectstatic --noinput 2>/dev/null || \
su -s /bin/sh appuser -c "python manage.py collectstatic --noinput"

# Aplica las migraciones pendientes antes de levantar el servidor
su-exec appuser python manage.py migrate --noinput 2>/dev/null || \
su -s /bin/sh appuser -c "python manage.py migrate --noinput"

# Crea el superusuario administrador y el usuario gestor (idempotente)
su-exec appuser python manage.py create_initial_users 2>/dev/null || \
su -s /bin/sh appuser -c "python manage.py create_initial_users"

# Ejecuta el comando final (Gunicorn) como appuser
exec su -s /bin/sh appuser -c "$*"