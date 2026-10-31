from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"
    verbose_name="perfiles"

    def ready(self) -> None:
        import accounts.signals
