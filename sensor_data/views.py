from datetime import datetime, timedelta
from rest_framework_mongoengine import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SensorData, AutomationLog
from .serializers import SensorDataSerializer, AutomationLogSerializer
from django.shortcuts import get_object_or_404

class AutomationStatusView(APIView):
    def get(self, request, sensor_id):
        latest_data = SensorData.objects(sensor_id=sensor_id).order_by('-timestamp').first()
        if latest_data:
            return Response({
                "sensor_id": sensor_id,
                "type": latest_data.type,
                "value": latest_data.value,
                "timestamp": latest_data.timestamp,
                "location": latest_data.location,
                "details": {
                    "motion_detected": latest_data.motion_detected,
                    "temperature": latest_data.temperature,
                    "humidity": latest_data.humidity,
                    "voltage": latest_data.voltage,
                    "power": latest_data.power
                }
            })
        return Response({"error": "Aucune donnée trouvée"}, status=404)

class SensorListCreateView(generics.ListCreateAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

class SensorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    lookup_field = 'sensor_id'

class SensorDataBySensorView(generics.ListAPIView):
    serializer_class = SensorDataSerializer

    def get_queryset(self):
        sensor_id = self.kwargs['sensor_id']
        return SensorData.objects.filter(sensor_id=sensor_id).order_by('-timestamp')

class AutomationHistoryView(generics.ListAPIView):
    serializer_class = AutomationLogSerializer
    
    def get_queryset(self):
        hours = int(self.request.query_params.get('hours', 24))
        since = datetime.now() - timedelta(hours=hours)
        return AutomationLog.objects.filter(timestamp__gte=since).order_by('-timestamp')

class EnergyStatsView(APIView):
    def get(self, request):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        total_energy = SensorData.objects(
            type="PZEM",
            timestamp__gte=today
        ).sum('energy')
        
        savings = AutomationLog.objects(
            action__in=["OFF", "DIM"],
            timestamp__gte=today
        ).count() * 0.05
        
        return Response({
            "total_energy_kwh": total_energy / 1000,
            "estimated_savings_kwh": savings,
            "automation_actions_today": AutomationLog.objects(timestamp__gte=today).count()
        })