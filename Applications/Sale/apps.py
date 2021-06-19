from django.apps import AppConfig


class SaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Applications.Sale'

    def ready(self):
        import Applications.Sale.signals