from django.apps import AppConfig


class AdsoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adso_app'

    def ready(self):
        import adso_app.signals  # Registra las señales