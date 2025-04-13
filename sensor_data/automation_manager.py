from .rules_engine import (
    update_last_pir_activity,
    rule_light_off_if_no_presence,
    rule_ac_off_if_window_open,
    rule_alert_or_cut_if_gas_detected,
    rule_dim_lights_based_on_ldr,
    rule_ac_on_if_hot,
    rule_light_on_if_presence_and_dark,
    rule_alert_high_power,
    rule_set_ac_eco_mode_if_idle,
    rule_ac_off_if_window_open
)

def apply_automation_rules(mqtt_client, data):
    if "PIR" in data:
        update_last_pir_activity(data["PIR"].get("value"))

    rule_light_off_if_no_presence(mqtt_client, data)
    rule_ac_off_if_window_open(mqtt_client, data)
    rule_alert_or_cut_if_gas_detected(mqtt_client, data)
    rule_dim_lights_based_on_ldr(mqtt_client, data)
    rule_ac_on_if_hot(mqtt_client, data)
    rule_light_on_if_presence_and_dark(mqtt_client, data)
    rule_alert_high_power(mqtt_client, data)
    rule_set_ac_eco_mode_if_idle(mqtt_client, data)