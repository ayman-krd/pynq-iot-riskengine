# Installation

This document explains how to install and configure the project on a PYNQ-Z2 board and a Windows PC running InfluxDB 2.x.

---

## 1. Requirements

- PYNQ-Z2 board with the official PYNQ image on a microSD card.
- USB cable (PROG/UART) and Ethernet cable.
- Windows PC with:
  - Python 3 on the PYNQ image,
  - InfluxDB 2.x installed.
- Basic electronics: photoresistor, thermistor, tilt switch or button, resistors.

---

## 2. PYNQ-Z2 setup

1. Insert the PYNQ image microSD card into the PYNQ-Z2.
2. Set the boot mode jumper to SD and the power source to USB.
3. Connect:
   - micro-USB (PROG/UART) from PYNQ-Z2 to the PC,
   - Ethernet cable between PYNQ-Z2 and PC (or the same router/switch).
4. Power on the board and wait for system to boot.

### 2.1 Network configuration (example)

Typical lab setup:

- PYNQ-Z2: `192.168.2.99`
- PC: `192.168.2.1` (IPv4 address on the Ethernet adapter, subnet mask `255.255.255.0`)

Then open in your browser:
Log in to Jupyter with the default password: xilinx
```text
http://192.168.2.99:9090

