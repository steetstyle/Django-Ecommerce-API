from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        from core.signals import cas_user_authenticated_callback, cas_user_logout_callback
        return super().ready()
