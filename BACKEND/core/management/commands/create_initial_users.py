import os

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

# Usuarios creados al levantar el contenedor.
# Se pueden personalizar con variables de entorno (ver .env).
INITIAL_USERS = [
    {
        "username": os.getenv("DJANGO_SUPERUSER_USERNAME", "admin"),
        "email": os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com"),
        "password": os.getenv("DJANGO_SUPERUSER_PASSWORD", "Admin12345!"),
        "group": "administrador",
        "is_superuser": True,
        "is_staff": True,
    },
    {
        "username": os.getenv("GESTOR_USERNAME", "gestor"),
        "email": os.getenv("GESTOR_EMAIL", "gestor@example.com"),
        "password": os.getenv("GESTOR_PASSWORD", "Gestor12345!"),
        "group": "gestor",
        "is_superuser": False,
        "is_staff": False,
    },
]


class Command(BaseCommand):
    help = "Crea el superusuario administrador y el usuario gestor si no existen."

    def handle(self, *args, **options):
        for data in INITIAL_USERS:
            if not data["username"] or not data["password"]:
                self.stdout.write(
                    self.style.WARNING(
                        "Se omitió un usuario inicial porque falta su nombre o contraseña."
                    )
                )
                continue

            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={"email": data["email"]},
            )

            if created:
                user.email = data["email"]
                user.is_superuser = data["is_superuser"]
                user.is_staff = data["is_staff"]
                user.set_password(data["password"])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Usuario '{user.username}' creado.")
                )
            else:
                # Aseguramos los permisos aunque el usuario ya existiera.
                user.is_superuser = data["is_superuser"]
                user.is_staff = data["is_staff"]
                user.save(update_fields=["is_superuser", "is_staff"])
                self.stdout.write(
                    f"Usuario '{user.username}' ya existe, se omite la creación."
                )

            group, _ = Group.objects.get_or_create(name=data["group"])
            # Dejamos únicamente el rol que corresponde (quita 'clientes', etc.).
            user.groups.set([group])
            self.stdout.write(
                f"  Rol asignado: {group.name}"
            )
