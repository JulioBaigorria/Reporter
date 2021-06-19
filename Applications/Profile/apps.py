from django.apps import AppConfig

class ProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Applications.Profile'

    def ready(self):
        import Applications.Profile.signals
