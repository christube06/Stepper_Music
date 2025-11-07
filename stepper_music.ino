// Stepper 28BYJ-48 + ULN2003
// PIN: IN1=4, IN2=5, IN3=6, IN4=7

#define IN1 4
#define IN2 5
#define IN3 6
#define IN4 7

// 8-step sequence for 28BYJ-48
const int sequence[8][4] = {
  {1,0,0,1},
  {1,0,0,0},
  {1,1,0,0},
  {0,1,0,0},
  {0,1,1,0},
  {0,0,1,0},
  {0,0,1,1},
  {0,0,0,1}
};

int stepIndex = 0;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}


void stepOne() {
  digitalWrite(IN1, sequence[stepIndex][0]);
  digitalWrite(IN2, sequence[stepIndex][1]);
  digitalWrite(IN3, sequence[stepIndex][2]);
  digitalWrite(IN4, sequence[stepIndex][3]);
  stepIndex++;
  if (stepIndex >= 8) stepIndex = 0;
}


void playNote(float freq, int duration_ms) {
  if (freq <= 0) {
    // Pause (0 Hz)
    delay(duration_ms);
    return;
  }

  
  float period = 1000000.0 / freq;

  unsigned long endTime = millis() + duration_ms;

  
  while (millis() < endTime) {
    stepOne();
    delayMicroseconds(period / 8);
  }
}

// HERE YOU PUT THE MELODY AND DURATION LISTS

float melody[] = {262, 294, 330, 349, 392, 440, 494};

int durations[] = {100,100,100,100,100,100,100,100};


void loop() {
  int notes = sizeof(melody) / sizeof(melody[0]);

  for (int i = 0; i < notes; i++) {
    playNote(melody[i], durations[i]);


    if (melody[i] > 0)
      delay(20);
  }

  // Wait before repeating the melody
  delay(1500);
}
