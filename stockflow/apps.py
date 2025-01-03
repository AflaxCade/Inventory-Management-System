from django.apps import AppConfig


class StockflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockflow'

    def ready(self):
        import stockflow.signals
