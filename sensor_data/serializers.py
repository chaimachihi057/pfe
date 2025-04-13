from rest_framework_mongoengine import serializers
from .models import SensorData, AutomationLog

class SensorDataSerializer(serializers.DocumentSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

class AutomationLogSerializer(serializers.DocumentSerializer):
    class Meta:
        model = AutomationLog
        fields = '__all__'