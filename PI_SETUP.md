# Raspberry Pi Setup Guide

This guide explains how to set up the Raspberry Pi for the Smart Traffic Management System.

## Prerequisites

- Raspberry Pi (any model with USB ports and network capability)
- microSD card (8GB or larger) with Raspberry Pi OS installed
- Internet connection
- Keyboard, mouse, and monitor (for initial setup) or SSH access

## Initial Setup

### 1. Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Python Dependencies
```bash
pip3 install pyserial flask flask-cors firebase-admin
```

Or using the requirements file:
```bash
pip3 install -r requirements.txt
```

### 3. Enable Serial Communication
```bash
sudo raspi-config
```
Navigate to:
- Interfacing Options → Serial
- Enable serial interface
- Reboot when prompted

## Configuration

### 1. Identify Arduino Ports
Connect both Arduinos to the Raspberry Pi and identify their ports:
```bash
ls /dev/ttyACM*
```

You should see two ports like:
```
/dev/ttyACM0
/dev/ttyACM1
```

### 2. Update Port Configuration
Edit [traffic_monitor.py](Raspberry%20pi%20Script/traffic_monitor.py) to match your Arduino ports:
```python
SENSOR_PORT = '/dev/ttyACM0'  # Sensor Arduino
LED_PORT = '/dev/ttyACM1'     # LED Arduino
```

Note: The order might vary depending on connection sequence. You can identify which is which by disconnecting one Arduino at a time and checking which port disappears.

### 3. Configure Firebase (Optional)
To enable data logging to Firebase:

1. Create a Firebase project at https://console.firebase.google.com/
2. Generate a service account key:
   - Project Settings → Service Accounts → Generate New Private Key
3. Save the JSON file as `firebase_creds.json` in the Raspberry Pi Script directory
4. Update the database URL in [traffic_monitor.py](Raspberry%20pi%20Script/traffic_monitor.py):
   ```python
   firebase_admin.initialize_app(cred, {
       'databaseURL': 'https://your-project-id-default-rtdb.firebaseio.com/'
   })
   ```

If you don't want to use Firebase, you can comment out the Firebase-related code in the script.

## Running the System

### 1. Start the Traffic Controller
```bash
cd "Raspberry pi Script"
python3 traffic_monitor.py
```

On successful startup, you should see:
```
Connected: /dev/ttyACM0
Connected: /dev/ttyACM1
DASHBOARD: http://YOUR_PI_IP:5000
```

### 2. Access the Web Dashboard
Open a web browser and navigate to:
```
http://YOUR_PI_IP_ADDRESS:5000
```

Replace `YOUR_PI_IP_ADDRESS` with your Raspberry Pi's IP address.

You can find your Pi's IP address with:
```bash
hostname -I
```

## System Architecture

### Main Components

1. **Serial Communication**
   - Communicates with both Arduinos via USB
   - Handles reconnection if an Arduino is disconnected

2. **Traffic Logic**
   - Implements dynamic timing algorithm
   - Manages state transitions (Red → Green → Yellow → Red)
   - Supports manual override

3. **Web Server**
   - Flask-based REST API for dashboard communication
   - Serves the React dashboard
   - Provides endpoints for manual control

### Data Flow

```
Sensor Arduino → Raspberry Pi (Serial) → Traffic Logic → LED Arduino (Serial) → Traffic Lights
                                      ↓
                                Web Dashboard (HTTP)
                                      ↓
                               Firebase (Optional)
```

## API Endpoints

### GET `/api/status`
Returns current system status:
```json
{
  "densities": {"lane0": 2, "lane1": 0, "lane2": 1, "lane3": 3},
  "light": {"lane0": "Green", "lane1": "Red", "lane2": "Red", "lane3": "Red"},
  "timer": {"lane0": 25.3, "lane1": 0, "lane2": 0, "lane3": 0},
  "timer_state": {"lane0": "Green", "lane1": "", "lane2": "", "lane3": ""},
  "green_time": {"lane0": 35, "lane1": 15, "lane2": 25, "lane3": 45}
}
```

### POST `/api/manual`
Controls manual mode:
```json
// Force green for lane 0
{
  "lane": 0
}

// Resume smart mode
{
  "lane": null
}
```

## Auto-start on Boot

To automatically start the traffic system on boot:

### 1. Create a systemd service
```bash
sudo nano /etc/systemd/system/traffic-system.service
```

Add the following content:
```ini
[Unit]
Description=Smart Traffic Management System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/IOT_Project_smart traffic/Raspberry pi Script
ExecStart=/usr/bin/python3 traffic_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Enable the service
```bash
sudo systemctl enable traffic-system.service
sudo systemctl start traffic-system.service
```

### 3. Check status
```bash
sudo systemctl status traffic-system.service
```

## Troubleshooting

### Common Issues

1. **Serial Port Permission Denied**
   ```bash
   sudo usermod -a -G dialout pi
   sudo chmod 666 /dev/ttyACM*
   ```
   Then reboot the Pi.

2. **Firebase Authentication Error**
   - Ensure `firebase_creds.json` is in the correct directory
   - Verify the database URL is correct
   - Check internet connectivity

3. **Dashboard Not Loading**
   - Check if the Flask server is running
   - Verify the IP address and port
   - Ensure the build directory exists in the traffic-dashboard folder

4. **Arduinos Not Detected**
   - Check USB connections
   - Verify serial communication is enabled
   - Try different USB ports

5. **Incorrect Lane Detection**
   - Verify IR sensor wiring
   - Check sensor Arduino code pin assignments
   - Test sensors individually

### Logs and Debugging

The system outputs logs to the console which can help diagnose issues:
- Connection status for both Arduinos
- Sensor data readings
- State transitions
- Error messages

To view logs when running as a service:
```bash
sudo journalctl -u traffic-system.service -f
```

### Testing Individual Components

1. **Test Serial Connection**
   ```bash
   screen /dev/ttyACM0 9600
   ```
   Send commands manually to test LED Arduino response.

2. **Test Sensor Data**
   Open Arduino Serial Monitor for the sensor Arduino to verify data output.

3. **Test API Endpoints**
   ```bash
   curl http://localhost:5000/api/status
   ```