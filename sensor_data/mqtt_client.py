import paho.mqtt.client as mqtt
import json
import time
import uuid
import threading
from typing import Dict, Any
from django.conf import settings
from sensor_data.tasks import save_sensor_data

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(client_id=f"sensor_client_{uuid.uuid4().hex[:8]}")
        self.connected = False
        self.sensor_ids = {
            "LDR": None,
            "MQ2": None,
            "PZEM": None,
            "PIR": None,
            "DHT22": None,
        }
        
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        self.broker = settings.MQTT_BROKER
        self.port = settings.MQTT_PORT
        self.topic = settings.MQTT_TOPIC
        self.keepalive = settings.MQTT_KEEPALIVE
        self.max_retries = settings.MQTT_MAX_RETRIES
        
        if hasattr(settings, 'MQTT_USERNAME'):
            self.client.username_pw_set(
                settings.MQTT_USERNAME,
                settings.MQTT_PASSWORD
            )
        
        if getattr(settings, 'MQTT_USE_TLS', False):
            self.client.tls_set()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
          self.connected = True
          print(f"Connecté au broker MQTT {self.broker}:{self.port}")
          self.client.subscribe(self.topic)
        else:
          print(f"Échec de connexion au broker MQTT, code : {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        if rc != 0:
            self.connect_with_retry()

    def _on_message(self, client, userdata, message):
        from sensor_data.automation_manager import apply_automation_rules
        
        try:
            payload = message.payload.decode("utf-8")
            data_raw = json.loads(payload)
            location = self._get_location_from_topic(message.topic)
            automation_data = {}
            
            if "light_value" in data_raw:
                self._process_ldr(data_raw, location, automation_data)
            elif "MQ2" in data_raw:
                self._process_mq2(data_raw, location, automation_data)
            elif "voltage" in data_raw:
                self._process_pzem(data_raw, location, automation_data)
            elif "motion_detected" in data_raw:
                self._process_pir({"motion": data_raw["motion_detected"]}, location, automation_data)
            elif "temperature" in data_raw:
                self._process_dht22(data_raw, location, automation_data)
            
            if automation_data:
                apply_automation_rules(self.client, automation_data)
                
        except Exception:
            pass


    def _process_ldr(self, data, location, automation_data):
        self.sensor_ids["LDR"] = self.sensor_ids["LDR"] or f"esp32_ldr_{uuid.uuid4().hex[:8]}"
        value = float(data["light_value"])
        save_sensor_data(
            sensor_id=self.sensor_ids["LDR"],
            sensor_type="LDR",
            value=value,
            location="salle1"
        )
        automation_data["LDR"] = {"sensor_id": self.sensor_ids["LDR"], "value": value}

    def _process_mq2(self, data, location, automation_data):
        self.sensor_ids["MQ2"] = self.sensor_ids["MQ2"] or f"esp32_mq2_{uuid.uuid4().hex[:8]}"
        value = float(data["MQ2"])
        save_sensor_data(
            sensor_id=self.sensor_ids["MQ2"],
            sensor_type="MQ2",
            value=value,
            location="salle1"
        )
        automation_data["MQ2"] = {"sensor_id": self.sensor_ids["MQ2"], "value": value}

    def _process_pzem(self, data, location, automation_data):
        self.sensor_ids["PZEM"] = self.sensor_ids["PZEM"] or f"esp32_pzem_{uuid.uuid4().hex[:8]}"
        required_keys = ["voltage", "current", "power", "energy", "frequency", "power_factor"]
        
        if all(key in data for key in required_keys):
            save_sensor_data(
                sensor_id=self.sensor_ids["PZEM"],
                sensor_type="PZEM",
                value=float(data["power"]),
                location=location,
                voltage=float(data["voltage"]),
                current=float(data["current"]),
                power=float(data["power"]),
                energy=float(data["energy"]),
                frequency=float(data["frequency"]),
                power_factor=float(data["power_factor"])
            )
            automation_data["PZEM"] = {
                "sensor_id": self.sensor_ids["PZEM"],
                "value": float(data["power"]),
                "voltage": float(data["voltage"]),
                "current": float(data["current"])
            }

    def _process_pir(self, data, location, automation_data):
        self.sensor_ids["PIR"] = self.sensor_ids["PIR"] or f"esp32_pir_{uuid.uuid4().hex[:8]}"
        value = int(data["motion"])
        save_sensor_data(
            sensor_id=self.sensor_ids["PIR"],
            sensor_type="PIR",
            value=value,
            location="salle1"
        )
        automation_data["PIR"] = {"sensor_id": self.sensor_ids["PIR"], "value": value}

    def _process_dht22(self, data, location, automation_data):
        self.sensor_ids["DHT22"] = self.sensor_ids["DHT22"] or f"esp32_dht22_{uuid.uuid4().hex[:8]}"
        temp = float(data["temperature"])
        humidity = float(data["humidity"])
        save_sensor_data(
            sensor_id=self.sensor_ids["DHT22"],
            sensor_type="DHT22",
            value=temp,
            location="salle1",
            humidity=humidity
        )
        automation_data["DHT22"] = {
            "sensor_id": self.sensor_ids["DHT22"],
            "value": temp,
            "humidity": humidity
        }

    def _get_location_from_topic(self, topic):
        parts = topic.split('/')
        return parts[1] if len(parts) > 1 else "default"

    def connect_with_retry(self):
        retry_count = 0
        while retry_count < self.max_retries and not self.connected:
            try:
                self.client.connect(self.broker, self.port, self.keepalive)
                return True
            except Exception:
                retry_count += 1
                time.sleep(5)
        return False

    def start(self):
        return self.connect_with_retry()

mqtt_client = MQTTClient()

def start_mqtt_client():
    def run_mqtt_loop():
        if mqtt_client.start():
            while True:
                mqtt_client.client.loop(0.1)

    mqtt_thread = threading.Thread(target=run_mqtt_loop, daemon=True)
    mqtt_thread.start()