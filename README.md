# Smart Traffic Management System

![Smart Traffic System](Screenshot%202025-11-05%20162340.png)

An IoT-based smart traffic management system that uses Arduino sensors to detect vehicle density and dynamically adjusts traffic light timing to optimize traffic flow.

## 🚦 Project Overview

This project implements an intelligent traffic light control system that:
- Uses IR sensors to detect vehicle density on each lane
- Dynamically adjusts green light duration based on traffic density
- Provides a real-time web dashboard for monitoring and control
- Supports both automatic smart mode and manual override

### 🏗️ System Architecture

```
IR Sensors (Arduino 1) → Raspberry Pi → Traffic Light Control (Arduino 2) → Web Dashboard
         ↓
    [Vehicle Density Data] → Dynamic Timing Algorithm → [Traffic Light Control]
```

## 📁 Project Structure

```
.
├── Arduino codes/
│   ├── sensor_arduino.ino     # Controls IR sensors for vehicle detection
│   └── led_arduino.ino        # Controls traffic lights
├── Raspberry pi Script/
│   └── traffic_monitor.py     # Main control script with Flask web server
├── traffic-dashboard/         # React web dashboard
├── IOT_Circuit Diagram_Final_bb.png  # Circuit diagram
└── Screenshot 2025-11-05 162340.png   # Dashboard screenshot
```

## 🛠️ Hardware Components

1. **2 Arduino Boards**
   - Arduino 1: Connects 12 IR sensors (3 per lane) for vehicle detection
   - Arduino 2: Controls 4 traffic lights (12 LEDs - Red, Yellow, Green per lane)

2. **Raspberry Pi**
   - Acts as the central controller
   - Hosts the web dashboard
   - Runs the Python control script

3. **IR Sensors**
   - 12 IR sensors total (3 per lane)
   - Detect vehicle presence on each lane

4. **LED Traffic Lights**
   - 4 sets of traffic lights (Red, Yellow, Green per lane)

## 🔧 How It Works

### Sensor Arduino (`sensor_arduino.ino`)
- Reads data from 12 IR sensors (3 per lane)
- Calculates vehicle density for each of the 4 lanes
- Sends density data to Raspberry Pi via USB serial

### LED Arduino (`led_arduino.ino`)
- Receives commands from Raspberry Pi via USB serial
- Controls the traffic lights based on received commands
- Supports commands for individual lane control and all-red state

### Raspberry Pi Controller (`traffic_monitor.py`)
- Communicates with both Arduinos via USB serial
- Implements dynamic traffic light timing algorithm
- Hosts a Flask web server for the dashboard
- Pushes data to Firebase for historical analysis

### Web Dashboard (`traffic-dashboard/`)
- Built with React.js
- Shows real-time vehicle density for each lane
- Displays current traffic light status with countdown timers
- Allows manual override of traffic light control

## 🚀 Setup Instructions

### Arduino Setup
1. Upload [sensor_arduino.ino](Arduino%20codes/sensor_arduino.ino) to the first Arduino
2. Upload [led_arduino.ino](Arduino%20codes/led_arduino.ino) to the second Arduino
3. Connect hardware as shown in the circuit diagram

### Raspberry Pi Setup
1. Install required Python packages:
   ```bash
   pip install pyserial flask flask-cors firebase-admin
   ```

2. Update serial port configurations in [traffic_monitor.py](Raspberry%20pi%20Script/traffic_monitor.py):
   ```python
   SENSOR_PORT = '/dev/ttyACM0'  # Adjust to your sensor Arduino port
   LED_PORT = '/dev/ttyACM1'     # Adjust to your LED Arduino port
   ```

3. Configure Firebase credentials:
   - Place your Firebase service account key as `firebase_creds.json`
   - Update the database URL in the script

4. Run the controller:
   ```bash
   python traffic_monitor.py
   ```

### Web Dashboard Setup
1. Navigate to the dashboard directory:
   ```bash
   cd traffic-dashboard
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Update the API endpoint in [App.js](traffic-dashboard/src/App.js):
   ```javascript
   const API = 'http://YOUR_PI_IP_ADDRESS:5000/api';
   ```

4. Build the dashboard:
   ```bash
   npm run build
   ```

5. The dashboard will be served by the Flask server

## 🌐 Web Interface

The dashboard provides:
- Real-time vehicle density visualization
- Traffic light status with countdown timers
- Manual override buttons for each lane
- "Resume Smart Mode" button

![Dashboard Screenshot](Screenshot%202025-11-05%20162340.png)

## ⚙️ Algorithm Details

The system uses a dynamic timing algorithm:
- Base green time: 15 seconds
- Additional time: 10 seconds × vehicle density
- Minimum green time: 5 seconds
- Fixed yellow time: 5 seconds

This ensures that busier lanes get more green time while preventing starvation of lighter lanes.

## 📊 Data Logging

The system logs traffic data to Firebase Realtime Database:
- Vehicle density for each lane
- Timestamped entries for historical analysis
- Non-blocking implementation to prevent delays

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Created as part of an IoT course project
- Inspired by real-world smart city initiatives