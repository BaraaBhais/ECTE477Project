#include <DHT.h>

#define DHT_PIN  4
#define LDR_PIN  A0
#define MQ2_PIN  A1
#define PIR_PIN  3

#define TEMP_THRESHOLD   30.0
#define GAS_THRESHOLD    400
#define LIGHT_THRESHOLD  300
#define NO_MOTION_DELAY  30000

DHT dht(DHT_PIN, DHT22);

int lightStatus = 0;
unsigned long lastMotionTime = 0;
bool motionActive = false;

void setup() {
  Serial.begin(9600);
  pinMode(PIR_PIN, INPUT);
  dht.begin();
  Serial.println("Smart Home Started");
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity    = dht.readHumidity();
  if (isnan(temperature)) temperature = 25.0;
  if (isnan(humidity))    humidity    = 50.0;

  int lightLevel = analogRead(LDR_PIN);
  int gasLevel   = analogRead(MQ2_PIN);
  int motion     = digitalRead(PIR_PIN);

  if (motion == 1) {
    lastMotionTime = millis();
    motionActive = true;
    if (lightLevel < LIGHT_THRESHOLD) lightStatus = 1;
  }
  if (motionActive && (millis() - lastMotionTime >= NO_MOTION_DELAY)) {
    lightStatus  = 0;
    motionActive = false;
  }

  if (temperature > TEMP_THRESHOLD) Serial.println("ALERT: FAN ON");
  if (gasLevel > GAS_THRESHOLD)     Serial.println("ALERT: FIRE/GAS EMERGENCY");

  Serial.print("{\"temp\":");        Serial.print(temperature, 1);
  Serial.print(",\"humidity\":");    Serial.print(humidity, 1);
  Serial.print(",\"light\":");       Serial.print(lightLevel);
  Serial.print(",\"motion\":");      Serial.print(motion);
  Serial.print(",\"gas\":");         Serial.print(gasLevel);
  Serial.print(",\"lightStatus\":"); Serial.print(lightStatus);
  Serial.println("}");

  delay(5000);
}
