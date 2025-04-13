from mongoengine import Document, fields
import datetime

class SensorData(Document):
    sensor_id = fields.StringField(max_length=50, unique=True, required=True)
    type = fields.StringField(max_length=50, choices=[
        ('LDR', 'LDR'),
        ('MQ2', 'MQ2'),
        ('DHT22', 'DHT22'),
        ('PIR', 'PIR'),
        ('PZEM', 'PZEM')
    ], required=True)
    value = fields.FloatField(required=True)
    timestamp = fields.DateTimeField(default=lambda: datetime.datetime.now())
    location = fields.StringField(max_length=100, required=True)
    voltage = fields.FloatField(required=False)
    current = fields.FloatField(required=False)
    power = fields.FloatField(required=False)
    energy = fields.FloatField(required=False)
    frequency = fields.FloatField(required=False)
    power_factor = fields.FloatField(required=False)
    temperature = fields.FloatField(required=False)
    humidity = fields.FloatField(required=False)
    motion_detected = fields.BooleanField(required=False, default=False)

    meta = {
        'collection': 'sensor_data',
        'ordering': ['-timestamp']
    }

    def __str__(self):
        return f"{self.sensor_id} - {self.value} at {self.location}"

class AutomationLog(Document):
    timestamp = fields.DateTimeField(default=lambda: datetime.datetime.now())
    device = fields.StringField(max_length=50, required=True)
    action = fields.StringField(max_length=50, required=True)
    reason = fields.StringField(max_length=200, required=True)

    meta = {
        'collection': 'automation_logs',
        'ordering': ['-timestamp']
    }

    def __str__(self):
        return f"{self.device} - {self.action} - {self.reason} at {self.timestamp}"