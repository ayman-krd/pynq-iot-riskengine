# IoT risk monitoring system on PYNQ-Z2

This repository contains a small IoT-style monitoring system implemented on a PYNQ-Z2 board using Python.

The system:

- Reads three sensors connected to the Arduino header:
  - A0: light sensor (photoresistor).
  - A1: temperature sensor (thermistor).
  - A2: event sensor (tilt switch or push button).

- Computes a **risk level** (0 to 3) in Python based on thresholds on the three sensors.

- Shows the risk level on the **on-board LEDs** of the PYNQ-Z2:
  - Risk 0 → all LEDs off.
  - Risk 1 → LED0 on.
  - Risk 2 → LED0 and LED1 on.
  - Risk 3 → LED0, LED1 and LED2 on.

- Sends all measurements (raw sensor values, risk level and alert flags) to **InfluxDB 2.x**, where they can be visualized and used to define alert rules.

---

## Repository structure

- `sw/python/main.py`  
  Main Python script that runs on the PYNQ-Z2:
  - loads the `base.bit` overlay,
  - reads A0, A1, A2 via `Arduino_Analog`,
  - computes the risk level and updates the on-board LEDs,
  - sends the data to InfluxDB using the HTTP API.

- `docs/installation.md`  
  Step-by-step installation guide:
  - PYNQ image and network configuration,
  - Python dependencies on the board,
  - InfluxDB 2.x installation and initial setup on Windows.

- `docs/usage.md`  
  How to connect the sensors, run the script on the PYNQ and visualize the data in InfluxDB.

- `docs/iotpynq.pdf`  
  Slides used for the class presentation (architecture, diagrams, screenshots and demo explanation).

---

## Quick start

1. Follow `docs/installation.md` to:
   - prepare the PYNQ-Z2 board,
   - install the required Python packages,
   - install and set up InfluxDB 2.x on a Windows PC.

2. Copy or clone this repository onto the PYNQ-Z2 (for example into the Jupyter notebooks directory).

3. Edit `sw/python/main.py` on the PYNQ and set your InfluxDB configuration:

   ```python
   INFLUX_URL = "http://<PC_IP>:8086/api/v2/write"
   INFLUX_ORG = "<your_org_name>"
   INFLUX_BUCKET = "<your_bucket_name>"
   INFLUX_TOKEN = "PUT_YOUR_TOKEN_HERE"

