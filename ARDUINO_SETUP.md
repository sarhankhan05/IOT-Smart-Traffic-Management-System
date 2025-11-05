# Arduino Setup Guide

This guide explains how to set up both Arduino boards for the Smart Traffic Management System.

## Sensor Arduino Setup

### Components Needed
- 1 Arduino Uno/Nano
- 12 IR sensors (3 per lane)
- Jumper wires
- Breadboard (optional)

### Pin Connections

| Function | Pin |
|----------|-----|
| Lane 0 IR Sensor 1 | Digital Pin 2 |
| Lane 0 IR Sensor 2 | Digital Pin 3 |
| Lane 0 IR Sensor 3 | Digital Pin 4 |
| Lane 1 IR Sensor 1 | Digital Pin 5 |
| Lane 1 IR Sensor 2 | Digital Pin 6 |
| Lane 1 IR Sensor 3 | Digital Pin 7 |
| Lane 2 IR Sensor 1 | Digital Pin 8 |
| Lane 2 IR Sensor 2 | Digital Pin 9 |
| Lane 2 IR Sensor 3 | Digital Pin 10 |
| Lane 3 IR Sensor 1 | Digital Pin 11 |
| Lane 3 IR Sensor 2 | Digital Pin 12 |
| Lane 3 IR Sensor 3 | Digital Pin 13 |

### Code Installation
1. Open [sensor_arduino.ino](Arduino%20codes/sensor_arduino.ino) in Arduino IDE
2. Connect the Arduino to your computer via USB
3. Select the correct board and port in Arduino IDE
4. Upload the code to the Arduino

### How It Works
- The sensor Arduino reads all 12 IR sensors every 200ms
- For each lane, it counts how many sensors detect vehicles (0-3)
- This density data is sent to the Raspberry Pi via serial communication in the format:
  ```
  LANE0:2;LANE1:0;LANE2:1;LANE3:3;
  ```

## LED Arduino Setup

### Components Needed
- 1 Arduino Uno/Nano
- 12 LEDs (4 sets of Red, Yellow, Green)
- 12 Resistors (220Ω)
- Jumper wires
- Breadboard

### Pin Connections

| Traffic Light | Pin |
|---------------|-----|
| Lane 0 Red | Digital Pin 2 |
| Lane 0 Yellow | Digital Pin 3 |
| Lane 0 Green | Digital Pin 4 |
| Lane 1 Red | Digital Pin 5 |
| Lane 1 Yellow | Digital Pin 6 |
| Lane 1 Green | Digital Pin 7 |
| Lane 2 Red | Digital Pin 8 |
| Lane 2 Yellow | Digital Pin 9 |
| Lane 2 Green | Digital Pin 10 |
| Lane 3 Red | Digital Pin 11 |
| Lane 3 Yellow | Digital Pin 12 |
| Lane 3 Green | Digital Pin 13 |

### Circuit Diagram
Refer to [IOT_Circuit Diagram_Final_bb.png](IOT_Circuit Diagram_Final_bb.png) for the complete wiring diagram.

### Code Installation
1. Open [led_arduino.ino](Arduino%20codes/led_arduino.ino) in Arduino IDE
2. Connect the Arduino to your computer via USB
3. Select the correct board and port in Arduino IDE
4. Upload the code to the Arduino

### Supported Commands
The LED Arduino accepts the following serial commands:

| Command | Action |
|---------|--------|
| `ALL:R` | Sets all lanes to red light |
| `LANE0:G` | Sets lane 0 to green light |
| `LANE0:Y` | Sets lane 0 to yellow light |
| `LANE0:R` | Sets all lanes to red light (safety measure) |
| Similar commands for lanes 1, 2, and 3 |

### How It Works
- The LED Arduino listens for serial commands from the Raspberry Pi
- When a command is received, it updates the traffic lights accordingly
- In green mode, only the specified lane gets green, others remain red
- In yellow mode, the specified lane gets yellow, others remain red
- The `ALL:R` command is used for safety transitions

## Troubleshooting

### Common Issues

1. **No Communication**
   - Check USB connections between Arduino and Raspberry Pi
   - Verify serial port settings in [traffic_monitor.py](Raspberry%20pi%20Script/traffic_monitor.py)
   - Ensure both Arduinos are powered properly

2. **Incorrect Sensor Readings**
   - Check IR sensor wiring
   - Ensure sensors are positioned correctly to detect vehicles
   - Verify that sensor pins in the code match physical connections

3. **Lights Not Responding**
   - Check LED wiring and resistor connections
   - Verify LED pins in the code match physical connections
   - Ensure the Arduino is receiving power

4. **Inconsistent Behavior**
   - Check for loose connections
   - Ensure adequate power supply to all components
   - Restart all devices in order: Sensors → LED Arduino → Raspberry Pi

### Testing

1. **Sensor Test**
   - Open Arduino Serial Monitor
   - Set baud rate to 9600
   - Observe sensor data output

2. **LED Test**
   - Open Arduino Serial Monitor
   - Set baud rate to 9600
   - Send `LANE0:G` and observe if lane 0 turns green
   - Send `ALL:R` and observe if all lanes turn red