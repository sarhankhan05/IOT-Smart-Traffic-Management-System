#define NUM_LANES 4

// LED Pins: {Red, Yellow, Green} - Using D2-D13
int ledPins[NUM_LANES][3] = {
  {2, 3, 4},   // Lane 0: North
  {5, 6, 7},   // Lane 1: East
  {8, 9, 10},  // Lane 2: South
  {11, 12, 13} // Lane 3: West
};

void setup() {
  Serial.begin(9600);

  // Initialize LED pins
  for (int lane = 0; lane < NUM_LANES; lane++) {
    for (int i = 0; i < 3; i++) {
      pinMode(ledPins[lane][i], OUTPUT);
      digitalWrite(ledPins[lane][i], LOW);
    }
  }
  setAllRed(); // Start with all red
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
      else if (state == 'R') setAllRed(); 
    }
  }
}

void setAllRed() {
  for (int l = 0; l < NUM_LANES; l++) {
    digitalWrite(ledPins[l][0], HIGH); // Red ON
    digitalWrite(ledPins[l][1], LOW);
    digitalWrite(ledPins[l][2], LOW);
  }
}

void setGreen(int lane) {
  for (int i = 0; i < NUM_LANES; i++) {
    digitalWrite(ledPins[i][0], (i == lane) ? LOW : HIGH); // Red OFF for green lane
    digitalWrite(ledPins[i][1], LOW);
    digitalWrite(ledPins[i][2], (i == lane) ? HIGH : LOW); // Green ON
  }
}

void setYellow(int lane) {
  for (int i = 0; i < NUM_LANES; i++) {
    digitalWrite(ledPins[i][0], (i == lane) ? LOW : HIGH);
    digitalWrite(ledPins[i][1], (i == lane) ? HIGH : LOW);
    digitalWrite(ledPins[i][2], LOW);
  }
}