from .models import SensorData

def save_sensor_data(sensor_id, sensor_type, value, location, **kwargs):
    sensor_data = SensorData(
        sensor_id=sensor_id,
        type=sensor_type,
        value=value,
        location=location,
        voltage=kwargs.get('voltage'),
        current=kwargs.get('current'),
        power=kwargs.get('power'),
        energy=kwargs.get('energy'),
        frequency=kwargs.get('frequency'),
        power_factor=kwargs.get('power_factor'),
        temperature=kwargs.get('temperature'),
        humidity=kwargs.get('humidity'),
        motion_detected=kwargs.get('motion_detected')
    )
    sensor_data.save()