# sensor_data/utils.py
def log_action(sensor_id, action, message):
    print(f"[ACTION] Sensor: {sensor_id} | {action} | {message}")