const int analogInPin = A0;  // Analog input para la señal

const int ledPin =  12;      // Salida digital para medir frecuencia de muestreo

int signal_read = 0;         // Variable para guardar la conversión AD

int state = 0;               // Variable de ayuda para salida digital

 

void setup() {

 

  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);

 

}

 

void loop() {

 

  signal_read = analogRead(analogInPin);

  Serial.println(signal_read);

  delay(1);

  digitalWrite(ledPin, (state) ? HIGH : LOW);

  state = !state;

 

}
