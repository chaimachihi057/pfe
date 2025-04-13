import datetime
import json
from django.conf import settings

LIGHT_BRIGHT_THRESHOLD = getattr(settings, "LIGHT_BRIGHT_THRESHOLD", 300)
LIGHT_DARK_THRESHOLD = getattr(settings, "LIGHT_DARK_THRESHOLD", 100)
TEMP_HIGH_THRESHOLD = getattr(settings, "TEMP_HIGH_THRESHOLD", 28.0)
HUMIDITY_WINDOW_THRESHOLD = getattr(settings, "HUMIDITY_WINDOW_THRESHOLD", 80.0)
GAS_THRESHOLD = getattr(settings, "GAS_THRESHOLD", 400)
POWER_HIGH_THRESHOLD = getattr(settings, "POWER_HIGH_THRESHOLD", 2000)
IDLE_TIMEOUT = getattr(settings, "IDLE_TIMEOUT", 900)
LIGHT_OFF_DELAY = getattr(settings, "LIGHT_OFF_DELAY", 300)

last_pir_activity = {"timestamp": datetime.datetime.now()}
last_ac_activity = {"timestamp": datetime.datetime.now()}

def update_last_pir_activity(pir_value):
    if pir_value == 1:
        last_pir_activity["timestamp"] = datetime.datetime.now()
        print(f"Activité PIR mise à jour : {last_pir_activity['timestamp']}")

def publish_control_message(mqtt_client, device, payload):
    topic = f"{settings.MQTT_CONTROL_TOPIC}/{device}"  # ex. "esp32/control/light"
    payload_str = json.dumps(payload)
    mqtt_client.publish(topic, payload_str)

def rule_light_off_if_no_presence(mqtt_client, data):
    pir_value = data.get("PIR", {}).get("value", 0)
    now = datetime.datetime.now()
    idle_time = (now - last_pir_activity["timestamp"]).total_seconds()
    print(f"Règle lumière éteinte : PIR={pir_value}, idle_time={idle_time}")
    
    if pir_value == 0 and idle_time > LIGHT_OFF_DELAY:
        publish_control_message(
            mqtt_client, 
            "light", 
            {"device": "light", "state": "off", "idle_time": idle_time}
        )

def rule_ac_off_if_window_open(mqtt_client, data):
    humidity = data.get("DHT22", {}).get("humidity", 0)
    print(f"Règle AC éteint : humidité={humidity}")
    if humidity > HUMIDITY_WINDOW_THRESHOLD:
        publish_control_message(
            mqtt_client, 
            "ac", 
            {"device": "ac", "state": "off", "reason": "high_humidity", "value": humidity}
        )

def rule_alert_or_cut_if_gas_detected(mqtt_client, data):
    mq2_value = data.get("MQ2", {}).get("value", 0)
    print(f"Règle gaz : MQ2={mq2_value}")
    if mq2_value > GAS_THRESHOLD:
        publish_control_message(
            mqtt_client,
            "main_power",
            {"device": "main_power", "state": "off", "alert": "gas_detected", "value": mq2_value}
        )

def rule_dim_lights_based_on_ldr(mqtt_client, data):
    if "LDR" in data and "PIR" in data:
        ldr_value = data["LDR"]["value"]
        pir_value = data["PIR"].get("value", 0)
        brightness = max(0, min(255, 255 - int((ldr_value / 1024) * 255)))
        print(f"Règle gradation : LDR={ldr_value}, PIR={pir_value}, brightness={brightness}")
        if pir_value == 1:
            publish_control_message(
                mqtt_client,
                "dimmer",
                {"device": "dimmer", "value": brightness, "ldr_value": ldr_value}
            )

def rule_ac_on_if_hot(mqtt_client, data):
    temp = data.get("DHT22", {}).get("temperature", 0)
    humidity = data.get("DHT22", {}).get("humidity", 0)
    print(f"Règle AC allumé : temp={temp}, humidité={humidity}")
    
    if temp > TEMP_HIGH_THRESHOLD and humidity < HUMIDITY_WINDOW_THRESHOLD:
        publish_control_message(
            mqtt_client,
            "ac",
            {"device": "ac", "state": "on", "mode": "cool", "target_temp": 22}
        )
        last_ac_activity["timestamp"] = datetime.datetime.now()

def rule_light_on_if_presence_and_dark(mqtt_client, data):
    pir_value = data.get("PIR", {}).get("value", 0)
    ldr_value = data.get("LDR", {}).get("value", 0)
    print(f"Règle lumière allumée : PIR={pir_value}, LDR={ldr_value}")
    
    if pir_value == 1 and ldr_value < LIGHT_DARK_THRESHOLD:
        publish_control_message(
            mqtt_client,
            "light",
            {"device": "light", "state": "on", "reason": "presence_in_dark"}
        )

def rule_alert_high_power(mqtt_client, data):
    power = data.get("PZEM", {}).get("power", 0)
    print(f"Règle alerte puissance : power={power}")
    if power > POWER_HIGH_THRESHOLD:
        publish_control_message(
            mqtt_client,
            "alert",
            {"device": "alert", "type": "high_power", "value": power}
        )

def rule_set_ac_eco_mode_if_idle(mqtt_client, data):
    now = datetime.datetime.now()
    idle_time = (now - last_ac_activity["timestamp"]).total_seconds()
    print(f"Règle mode éco : idle_time={idle_time}")
    
    if idle_time > IDLE_TIMEOUT:
        publish_control_message(
            mqtt_client,
            "ac",
            {"device": "ac", "mode": "eco", "target_temp": 25}
        )
