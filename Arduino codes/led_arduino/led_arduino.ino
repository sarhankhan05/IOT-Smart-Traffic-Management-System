#define NUM_LANES 4

<<<<<<< HEAD:Arduino codes/led_arduino/led_arduino.ino
// LED Pins: {Red, Yellow, Green} - Using D2-D13
=======
>>>>>>> 202deb6116a4ea65bd8b4d3a7c4a4d9d6fad8b6d:Arduino codes/led_arduino.ino
int ledPins[NUM_LANES][3] = {
  {2, 3, 4},   // Lane 0: North
  {5, 6, 7},   // Lane 1: East
  {8, 9, 10},  // Lane 2: South
  {11, 12, 13} // Lane 3: West
};

void setup() {
  Serial.begin(9600);

  for (int lane = 0; lane < NUM_LANES; lane++) {
    for (int i = 0; i < 3; i++) {
      pinMode(ledPins[lane][i], OUTPUT);
      digitalWrite(ledPins[lane][i], LOW);
    }
  }
  setAllRed(); 
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    execute(cmd);
  }
}

void execute(String cmd) {
  if (cmd == "ALL:R") {
    setAllRed();
  } else if (cmd.startsWith("LANE")) {
    int lane = cmd.substring(4, 5).toInt();
    char state = cmd[6];
    if (lane >= 0 && lane < 4) {
      if (state == 'G') setGreen(lane);
      else if (state == 'Y') setYellow(lane);
<<<<<<< HEAD:Arduino codes/led_arduino/led_arduino.ino
      else if (state == 'R') setAllRed(); 
=======
      else if (state == 'R') setAllRed();
>>>>>>> 202deb6116a4ea65bd8b4d3a7c4a4d9d6fad8b6d:Arduino codes/led_arduino.ino
    }
  }
}

void setAllRed() {
  for (int l = 0; l < NUM_LANES; l++) {
    digitalWrite(ledPins[l][0], HIGH); 
    digitalWrite(ledPins[l][1], LOW);
    digitalWrite(ledPins[l][2], LOW);
  }
}

void setGreen(int lane) {
  for (int i = 0; i < NUM_LANES; i++) {
    digitalWrite(ledPins[i][0], (i == lane) ? LOW : HIGH); 
    digitalWrite(ledPins[i][1], LOW);
    digitalWrite(ledPins[i][2], (i == lane) ? HIGH : LOW); 
  }
}

void setYellow(int lane) {
  for (int i = 0; i < NUM_LANES; i++) {
    digitalWrite(ledPins[i][0], (i == lane) ? LOW : HIGH);
    digitalWrite(ledPins[i][1], (i == lane) ? HIGH : LOW);
    digitalWrite(ledPins[i][2], LOW);
  }
}
