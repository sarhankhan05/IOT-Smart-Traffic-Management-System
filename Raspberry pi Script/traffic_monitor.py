# traffic_monitor.py
import serial, time, threading, os
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db

# === CONFIG ===
SENSOR_PORT = '/dev/ttyACM0'
LED_PORT = '/dev/ttyACM1'
cred = credentials.Certificate('firebase_creds.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://raspberry-sensordata-default-rtdb.firebaseio.com/'})
ref = db.reference('traffic_logs')

app = Flask(__name__)
CORS(app)


def push_to_firebase_async(data):
    
    try:
        human_readable_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_data = {**data, 'timestamp': human_readable_time}
        ref.push(log_data)
    except Exception as e:
        print(f"Firebase push error: {e}")

# === GLOBALS ===
last_densities = {"lane0": 0, "lane1": 0, "lane2": 0, "lane3": 0}
last_light = {"lane0": "Red", "lane1": "Red", "lane2": "Red", "lane3": "Red"}
timer_remaining = {"lane0": 0, "lane1": 0, "lane2": 0, "lane3": 0}
timer_state = {"lane0": "", "lane1": "", "lane2": "", "lane3": ""}
current_lane = 0
manual_mode = False
manual_thread = None
first_data_received = False
sensor_ser = None
led_ser = None 
smart_cycle_state = "ALL_RED"

def open_serial(port):
    while True:
        try:
            ser = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)
            print(f"Connected: {port}")
            return ser
        except:
            print(f"Waiting for {port}...")
            time.sleep(3)

# === START SERIAL ===
sensor_ser = open_serial(SENSOR_PORT)
led_ser = open_serial(LED_PORT)

def safe_write(data):
    global led_ser 
    try:
        led_ser.write(data)
    except:
        print("LED Arduino disconnected. Reconnecting...")
        led_ser = open_serial(LED_PORT)
        led_ser.write(data)

def parse_density(line):
    data = {}
    for part in line.strip().split(';'):
        if ':' in part and part:
            k, v = part.split(':')
            if k.startswith('LANE') and len(k) == 5:
                lane = int(k[4])
                if 0 <= lane < 4:
                    data[f'lane{lane}'] = int(v)
    return data

def sensor_thread():
    global last_densities, current_lane, manual_mode, first_data_received
    global timer_remaining, timer_state, smart_cycle_state

    last_time = time.time()

    while True:
        try:
            current_time = time.time()
            dt = current_time - last_time  
            last_time = current_time

            if sensor_ser.in_waiting:
                line = sensor_ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("LANE"):
                    new_d = parse_density(line)
                    if new_d:
                        
                        last_densities = {**last_densities, **new_d}

                        data_copy = last_densities.copy() 
                        threading.Thread(target=push_to_firebase_async, args=(data_copy,), daemon=True).start()
                        
                        
                        if not first_data_received:
                            first_data_received = True
                            print("FIRST DATA → STARTING CYCLE")

            
            for i in range(4):
                key = f'lane{i}'
                if timer_remaining[key] > 0:
                   
                    timer_remaining[key] -= dt 
                    if timer_remaining[key] <= 0:
                        timer_remaining[key] = 0
                        if timer_state[key] not in ["Green", "Yellow"]:
                            timer_state[key] = ""

            if not manual_mode and first_data_received:
                
                if smart_cycle_state == "ALL_RED":
                    if all(v <= 0 for v in timer_remaining.values()):
                        lane_key = f'lane{current_lane}'
                        density = last_densities.get(lane_key, 0)
                        green_time = max(5, 15 + density * 10)

                        timer_remaining[lane_key] = green_time
                        timer_state[lane_key] = "Green"
                        last_light[lane_key] = "Green"
                        safe_write(f"LANE{current_lane}:G\n".encode())
                        
                        smart_cycle_state = "GREEN"

                elif smart_cycle_state == "GREEN":
                    lane_key = f'lane{current_lane}'
                    if timer_remaining[lane_key] <= 0:
                        timer_remaining[lane_key] = 5
                        timer_state[lane_key] = "Yellow"
                        last_light[lane_key] = "Yellow"
                        safe_write(f"LANE{current_lane}:Y\n".encode())
                        
                        smart_cycle_state = "YELLOW"
                
                elif smart_cycle_state == "YELLOW":
                    lane_key = f'lane{current_lane}'
                    if timer_remaining[lane_key] <= 0:
                        safe_write(b"ALL:R\n")
                        for i in range(4):
                            last_light[f'lane{i}'] = "Red"
                            timer_state[f'lane{i}'] = ""
                            timer_remaining[f'lane{i}'] = 0
                        
                        current_lane = (current_lane + 1) % 4
                        smart_cycle_state = "ALL_RED"

        except Exception as e:
            print(f"Error in sensor_thread: {e}")

        time.sleep(0.05) 
      
threading.Thread(target=sensor_thread, daemon=True).start()

@app.route('/api/status')
def status():
    safe_d = {f'lane{i}': last_densities.get(f'lane{i}', 0) for i in range(4)}
    green_times = {f'lane{i}': max(5, 15 + safe_d[f'lane{i}'] * 10) for i in range(4)}
    return jsonify({
        "densities": safe_d,
        "light": last_light,
        "timer": timer_remaining,
        "timer_state": timer_state,
        "green_time": green_times
    })

@app.route('/api/manual', methods=['POST'])
def manual():
    global manual_mode, manual_thread, smart_cycle_state, current_lane
    
    lane = request.json.get('lane')
    
    if lane is None:
        manual_mode = False
        smart_cycle_state = "ALL_RED" 
        safe_write(b"ALL:R\n")
        for i in range(4):
            last_light[f'lane{i}'] = "Red"
            timer_state[f'lane{i}'] = ""
            timer_remaining[f'lane{i}'] = 0
        
        return jsonify({"ok": True, "action": "resuming_smart_mode"})

    manual_mode = True 
    
    active_lane = -1
    if (smart_cycle_state == "GREEN" or smart_cycle_state == "YELLOW") and timer_remaining[f'lane{current_lane}'] > 0:
        active_lane = current_lane
    
    smart_cycle_state = "ALL_RED" 
    
    def run_manual_sequence(forced_lane_str, active_lane_to_clear):
        global manual_mode, smart_cycle_state
        
        forced_lane = int(forced_lane_str)
        forced_key = f'lane{forced_lane}'
        
        try:
            if active_lane_to_clear != -1 and active_lane_to_clear != forced_lane:
                print(f"Clearing active lane {active_lane_to_clear} first...")
                active_key = f'lane{active_lane_to_clear}'
                
                timer_remaining[active_key] = 5
                timer_state[active_key] = "Yellow"
                last_light[active_key] = "Yellow"
                for i in range(4):
                    if i != active_lane_to_clear: last_light[f'lane{i}'] = "Red"
                
                safe_write(f"LANE{active_lane_to_clear}:Y\n".encode())
                
                start_yellow = time.time()
                while time.time() - start_yellow < 5:
                    timer_remaining[active_key] = 5 - (time.time() - start_yellow)
                    time.sleep(0.1)

            safe_write(b"ALL:R\n")
            for i in range(4):
                last_light[f'lane{i}'] = "Red"
                timer_state[f'lane{i}'] = ""
                timer_remaining[f'lane{i}'] = 0
            time.sleep(1)

            timer_remaining[forced_key] = 30
            timer_state[forced_key] = "Green"
            last_light[forced_key] = "Green"
            safe_write(f"LANE{forced_lane}:G\n".encode())

            start_green = time.time()
            while time.time() - start_green < 30:
                if not manual_mode: 
                    raise Exception("Manual mode cancelled")
                timer_remaining[forced_key] = 30 - (time.time() - start_green)
                time.sleep(0.1)

            timer_remaining[forced_key] = 5
            timer_state[forced_key] = "Yellow"
            last_light[forced_key] = "Yellow"
            safe_write(f"LANE{forced_lane}:Y\n".encode())
            
            start_yellow_2 = time.time()
            while time.time() - start_yellow_2 < 5:
                if not manual_mode:
                     raise Exception("Manual mode cancelled")
                timer_remaining[forced_key] = 5 - (time.time() - start_yellow_2)
                time.sleep(0.1)

        except Exception as e:
            print(f"Manual sequence error/interrupted: {e}")
        
        finally:
            safe_write(b"ALL:R\n")
            for i in range(4):
                last_light[f'lane{i}'] = "Red"
                timer_state[f'lane{i}'] = ""
                timer_remaining[f'lane{i}'] = 0
            
            manual_mode = False
            smart_cycle_state = "ALL_RED"
            print("Manual sequence finished. Resuming smart mode.")

    manual_thread = threading.Thread(target=run_manual_sequence, args=(lane, active_lane), daemon=True)
    manual_thread.start()
    
    return jsonify({"ok": True, "action": f"forcing_green_for_lane_{lane}"})    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join('dashboard', path)):
        return send_from_directory('dashboard', path)
    return send_from_directory('dashboard', 'index.html')

if __name__ == '__main__':
    print("DASHBOARD: http://10.81.93.84:5000")
    app.run(host='0.0.0.0', port=5000, threaded=True)
