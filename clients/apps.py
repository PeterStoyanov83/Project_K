from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clients'


class ClientsConfig(AppConfig):
    name = 'clients'

    def ready(self):
        import clients.signals