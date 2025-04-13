from django.apps import AppConfig

class SensorDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sensor_data'

    def ready(self):
        from .mqtt_client import start_mqtt_client
        start_mqtt_client()