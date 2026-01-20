# main.py
# IOT-style risk evaluation on PYNQ-Z2 using Arduino_Analog and on-board LEDs.
#
# Sensors (Arduino connector):
#   A0 -> light sensor (photoresistor)
#   A1 -> temperature sensor (thermistor)
#   A2 -> event sensor (tilt or button)
#
# Actuators (on-board):
#   base.leds[0..3] -> show risk level (0..3)

import time
import requests
from pynq.overlays.base import BaseOverlay
from pynq.lib.arduino import Arduino_Analog

# ----------------------------------------------------------------------
# InfluxDB 2.x configuration
# NOTE: Replace these placeholders with your real configuration
#       on the PYNQ board (do not commit secrets to GitHub).
# ----------------------------------------------------------------------
INFLUX_URL = "http://192.168.2.1:8086/api/v2/write"  # replace with your PC IP
INFLUX_ORG = "example_org"                           # replace with your org
INFLUX_BUCKET = "example_bucket"                     # replace with your bucket
INFLUX_TOKEN = "INFLUXDB_API_TOKEN_HERE"             # replace with your API token

MEASUREMENT = "pynq_sensors"
TAGS = "source=pynq_z2"

# ----------------------------------------------------------------------
# PYNQ and Arduino analog setup
# ----------------------------------------------------------------------

# Load base overlay
base = BaseOverlay("base.bit")

# Create Arduino analog object for A0, A1 and A2
# Index mapping:
#   0 -> A0 (light)
#   1 -> A1 (temperature)
#   2 -> A2 (event)
analog = Arduino_Analog(base.ARDUINO, [0, 1, 2])

print("Base overlay loaded and analog interface ready")

# ----------------------------------------------------------------------
# Thresholds for alert generation
# These values are based on typical idle readings and tuned for the demo.
# ----------------------------------------------------------------------
LIGHT_LOW_THR = 9500   # below this light_raw -> dark
TEMP_HIGH_THR = 9800   # above this temp_raw -> hot
EVENT_IDLE    = 150    # approximate idle value for event_raw
EVENT_DELTA   = 200    # deviation from idle -> event active

SAMPLE_PERIOD_SEC = 1.0


def read_sensors():
    """Read all sensors and return raw values: (light_raw, temp_raw, event_raw)."""
    raw_list = analog.read_raw()       # [A0_raw, A1_raw, A2_raw]
    light_raw = raw_list[0]           # A0
    temp_raw = raw_list[1]            # A1
    event_raw = raw_list[2]           # A2
    return light_raw, temp_raw, event_raw


def evaluate_risk(light_raw, temp_raw, event_raw):
    """
    Compute risk level and individual alerts.

    Returns:
        risk_level   (int): 0..3
        alert_light  (int): 0 or 1
        alert_temp   (int): 0 or 1
        alert_event  (int): 0 or 1
        alert_global (int): 0 or 1
    """
    # Light alert: dark environment
    alert_light = 1 if light_raw < LIGHT_LOW_THR else 0

    # Temperature alert: hot environment
    alert_temp = 1 if temp_raw > TEMP_HIGH_THR else 0

    # Event alert: event_raw moves far from idle value
    alert_event = 1 if abs(event_raw - EVENT_IDLE) > EVENT_DELTA else 0

    # Risk level is the number of active alerts (0..3)
    risk_level = alert_light + alert_temp + alert_event
    if risk_level > 3:
        risk_level = 3

    alert_global = 1 if risk_level > 0 else 0

    return risk_level, alert_light, alert_temp, alert_event, alert_global


def set_leds_by_risk(risk_level):
    """
    Set on-board LEDs according to risk level.

    Mapping:
        risk 0 -> all LEDs off
        risk 1 -> LED0 on
        risk 2 -> LED0 and LED1 on
        risk 3 -> LED0, LED1 and LED2 on
    """
    # Turn all LEDs off
    for led in base.leds:
        led.off()

    # Turn on LEDs according to risk level
    max_leds = len(base.leds)
    n = min(risk_level, max_leds)
    for i in range(n):
        base.leds[i].on()


def send_to_influx(light_raw, temp_raw, event_raw,
                   risk_level, alert_light, alert_temp,
                   alert_event, alert_global):
    """Send one sample to InfluxDB using line protocol."""

    params = {
        "org": INFLUX_ORG,
        "bucket": INFLUX_BUCKET,
        "precision": "s",
    }

    headers = {
        "Authorization": "Token " + INFLUX_TOKEN,
        "Content-Type": "text/plain",
    }

    # Line protocol fields (integers use suffix i)
    fields = (
        f"light_raw={light_raw}i,"
        f"temp_raw={temp_raw}i,"
        f"event_raw={event_raw}i,"
        f"risk_level={risk_level}i,"
        f"alert_light={alert_light}i,"
        f"alert_temp={alert_temp}i,"
        f"alert_event={alert_event}i,"
        f"alert_global={alert_global}i"
    )

    line = f"{MEASUREMENT},{TAGS} {fields}"

    try:
        resp = requests.post(
            INFLUX_URL,
            params=params,
            headers=headers,
            data=line,
            timeout=3.0,
        )
        print("Influx status:", resp.status_code)
    except Exception as e:
        print("Error sending to Influx:", e)


def main():
    """Main loop: read sensors, compute risk, update LEDs and send data."""
    print("Starting PYNQ risk monitor (analog sensors + on-board LEDs)")

    while True:
        # 1. Read sensors
        light_raw, temp_raw, event_raw = read_sensors()

        # 2. Evaluate risk
        risk_level, alert_light, alert_temp, alert_event, alert_global = \
            evaluate_risk(light_raw, temp_raw, event_raw)

        # 3. Print debug information
        print(
            "light={:5d} temp={:5d} event_raw={:5d} | "
            "risk={} global={} (L={} T={} E={})".format(
                light_raw, temp_raw, event_raw,
                risk_level, alert_global,
                alert_light, alert_temp, alert_event
            )
        )

        # 4. Set LEDs based on risk
        set_leds_by_risk(risk_level)

        # 5. Send data to InfluxDB
        send_to_influx(
            light_raw,
            temp_raw,
            event_raw,
            risk_level,
            alert_light,
            alert_temp,
            alert_event,
            alert_global,
        )

        # 6. Wait for next sample
        time.sleep(SAMPLE_PERIOD_SEC)


if __name__ == "__main__":
    main()
