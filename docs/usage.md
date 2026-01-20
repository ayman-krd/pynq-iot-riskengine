# Usage guide

This document explains how to connect the sensors, run the Python script on the PYNQ-Z2 and visualize the data in InfluxDB.

---

## 1. Hardware connections (PYNQ-Z2 Arduino header)

The system uses three analog inputs on the Arduino header of the PYNQ-Z2:

- A0: light sensor (photoresistor / LDR)
- A1: temperature sensor (NTC thermistor)
- A2: event sensor (tilt switch or push button)

All sensors are connected as simple voltage dividers or pull-up networks between 3.3 V and GND, with the middle node going to A0, A1 or A2.

> Important: all signals on the Arduino header must be 3.3 V. Do not use 5 V modules directly.

### 1.1 Light sensor (A0)

Use a photoresistor (LDR) and a fixed resistor (for example 10 kΩ):

- Connect one leg of the LDR to 3.3 V.
- Connect the other leg of the LDR to the middle node.
- Connect the middle node to A0.
- Connect the middle node to a 10 kΩ resistor, and the other end of the resistor to GND.

When there is light, the LDR resistance is low, the voltage on A0 is higher and `light_raw` is large. When you cover the LDR, the voltage on A0 decreases and `light_raw` becomes smaller.

### 1.2 Temperature sensor (A1)

Use an NTC thermistor and a fixed resistor (for example 10 kΩ):

- Connect one leg of the thermistor to 3.3 V.
- Connect the other leg of the thermistor to the middle node.
- Connect the middle node to A1.
- Connect the middle node to a 10 kΩ resistor, and the other end of the resistor to GND.

When you warm the thermistor with your fingers, its resistance changes and the voltage on A1 changes. The script uses a threshold on `temp_raw` to detect “high temperature”.

### 1.3 Event sensor (A2)

The event sensor is a simple tilt switch or push button, read as an analog value on A2:

- Connect one leg of the tilt switch / button to GND.
- Connect the other leg to **A2**.
- Add a **10 kΩ pull-up resistor** between A2 and 3.3 V.

In the idle state, the pull-up keeps A2 close to 3.3 V (high `event_raw`). When the tilt closes or the button is pressed, A2 is pulled to GND and `event_raw` becomes small. The script compares `event_raw` to an idle value and a delta to decide when the event is active.

### 1.4 Actuators

This version of the project uses the **on-board LEDs** of the PYNQ-Z2 as actuators:

- `base.leds[0]`, `base.leds[1]`, `base.leds[2]`, `base.leds[3]`

The LEDs are controlled directly in `main.py` and display the current risk level:

- Risk 0 → all LEDs off
- Risk 1 → LED0 on
- Risk 2 → LED0 and LED1 on
- Risk 3 → LED0, LED1 and LED2 on

## 2. Running the main script on the PYNQ-Z2

Before running the script, make sure that:

- InfluxDB 2.x is running on the Windows PC (for example at `http://localhost:8086`).
- The fields `INFLUX_URL`, `INFLUX_ORG`, `INFLUX_BUCKET` and `INFLUX_TOKEN` in `sw/python/main.py`
  have been configured according to `docs/installation.md`.

Typical example in `main.py`:

```python
   INFLUX_URL = "http://192.168.2.1:8086/api/v2/write"
   INFLUX_ORG = "Casa"
   INFLUX_BUCKET = "sensorica"
   INFLUX_TOKEN = "PUT_YOUR_TOKEN_HERE"
```

## 3. Open Jupyter in your browser(passsword=xilinx):

```text
   http://192.168.2.99:9090
```
- Navigate to the project folder, for example:
```text
   pynq-iot-riskengine/sw/python/
```
- Open a terminal (New → Terminal) or use a notebook cell and run:
```text
    cd /home/xilinx/jupyter_notebooks/pynq-iot-riskengine/sw/python
      python3 main.py
```
