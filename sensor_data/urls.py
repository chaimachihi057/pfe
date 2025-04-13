from django.urls import path
from .views import (
    SensorListCreateView,
    SensorDetailView,
    SensorDataBySensorView,
    AutomationStatusView,
    AutomationHistoryView,
    EnergyStatsView
)

urlpatterns = [
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('sensors/<str:sensor_id>/', SensorDetailView.as_view(), name='sensor-detail'),
    path('sensors/<str:sensor_id>/data/', SensorDataBySensorView.as_view(), name='sensor-data-by-sensor'),
    path('sensors/<str:sensor_id>/status/', AutomationStatusView.as_view(), name='automation-status'),
    path('automation/history/', AutomationHistoryView.as_view(), name='automation-history'),
    path('energy/stats/', EnergyStatsView.as_view(), name='energy-stats'),
]