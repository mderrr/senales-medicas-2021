
const int analogInPin = A0;  // Analog input para la señal
int signal_read = 0;         // Variable para guardar la conversión AD

void setup() {
  Serial.begin(115200);
}

void loop() { 
  signal_read = analogRead(analogInPin);
  Serial.println(signal_read);
  delay(100);
}
