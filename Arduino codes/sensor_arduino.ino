#define NUM_LANES 4
#define SENSORS_PER_LANE 3

int sensorPins[NUM_LANES][SENSORS_PER_LANE] = {
  {2, 3, 4}, {5, 6, 7}, {8, 9, 10}, {11, 12, 13}
};

int densities[NUM_LANES] = {0};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < NUM_LANES; i++) {
    for (int j = 0; j < SENSORS_PER_LANE; j++) {
      pinMode(sensorPins[i][j], INPUT);
    }
  }
}

void loop() {
  readSensors();
  sendToPi();
  delay(200);  
}

void readSensors() {
  for (int lane = 0; lane < NUM_LANES; lane++) {
    densities[lane] = 0;
    for (int s = 0; s < SENSORS_PER_LANE; s++) {
      if (digitalRead(sensorPins[lane][s]) == LOW) {
        densities[lane]++;
      }
    }
  }
}

void sendToPi() {
  String log = "";
  for (int i = 0; i < 4; i++) {
    log += "LANE" + String(i) + ":" + String(densities[i]) + ";";
  }
  Serial.println(log); 
  Serial.flush();
}
