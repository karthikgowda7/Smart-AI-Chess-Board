/*
 * sensor_test.ino - Smart AI Chess Board (ESP32)
 *
 * Minimal firmware to verify SS49E Hall sensors via CD74HC4067 multiplexer.
 *
 * Wiring:
 * 4067 SIG -> GPIO34 (Analog Read)
 * 4067 S0  -> GPIO25
 * 4067 S1  -> GPIO26
 * 4067 S2  -> GPIO27
 * 4067 S3  -> GPIO14
 *
 * SS49E #1 OUT -> 4067 C0
 * SS49E #2 OUT -> 4067 C1
 */

// Pin definitions
const int SIG_PIN = 34;
const int S0_PIN = 25;
const int S1_PIN = 26;
const int S2_PIN = 27;
const int S3_PIN = 14;

void setup() {
  // Initialize Serial Monitor at 115200 baud
  Serial.begin(115200);
  
  // Configure MUX select pins as outputs
  pinMode(S0_PIN, OUTPUT);
  pinMode(S1_PIN, OUTPUT);
  pinMode(S2_PIN, OUTPUT);
  pinMode(S3_PIN, OUTPUT);

  // Initial state (Channel 0)
  digitalWrite(S0_PIN, LOW);
  digitalWrite(S1_PIN, LOW);
  digitalWrite(S2_PIN, LOW);
  digitalWrite(S3_PIN, LOW);
  
  Serial.println("ESP32 Hall Sensor Test Started");
  Serial.println("==============================");
}

// Helper to select mux channel (0-15)
void selectMuxChannel(byte channel) {
  digitalWrite(S0_PIN, bitRead(channel, 0));
  digitalWrite(S1_PIN, bitRead(channel, 1));
  digitalWrite(S2_PIN, bitRead(channel, 2));
  digitalWrite(S3_PIN, bitRead(channel, 3));
}

void loop() {
  // 1. Select and read C0 (Hall 1)
  selectMuxChannel(0);
  delay(10); // Settling delay for analog read
  int valC0 = analogRead(SIG_PIN);
  
  // 2. Select and read C1 (Hall 2)
  selectMuxChannel(1);
  delay(10); // Settling delay for analog read
  int valC1 = analogRead(SIG_PIN);
  
  // 3. Print output clearly
  Serial.print("C0/HALL1: ");
  Serial.println(valC0);
  Serial.print("C1/HALL2: ");
  Serial.println(valC1);
  Serial.println("---");
  
  // 4. Delay to hit approximately 5 readings per second (200ms loop total)
  // We already delayed 20ms total (10ms + 10ms) above, so delay 180ms here.
  delay(180); 
}
