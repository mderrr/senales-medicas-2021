
const int analogInPin = A0;  // Analog input para la señal
int signal_read = 0;         // Variable para guardar la conversión AD
int muestras = 0;
int fs = 10;

void setup() {
  Serial.begin(115200);
}

void loop() { 
  digitalWrite(12, HIGH);
  digitalWrite(12, LOW);
  
  signal_read = analogRead(analogInPin);
  muestras += 1;
  Serial.println(signal_read);
  
  delay(1000 / fs);
}
