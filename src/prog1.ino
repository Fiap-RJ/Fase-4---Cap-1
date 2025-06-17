#include <DHT.h>
#include <DHT_U.h>

#include "Wire.h"
#include "LiquidCrystal_I2C.h"

#define DHTPIN 13       // Pino digital ao qual o sensor DHT22 está conectado
#define DHTTYPE DHT22   // Tipo de sensor DHT22

#define RELAY_PIN 19    // Pino digital ao qual o relé está conectado

#define pH 34    // Pino digital no qual o sensor LDR para pH está conectado

#define K 12        // Pino no qual o botao para detecção de Potassio (K)
#define P 27        // Pino no qual o botao para detecção de Fosforo (P)

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2); // Change to (0x27,20,4) for 20x4 LCD.

DHT_Unified dht(DHTPIN, DHTTYPE);

unsigned long delayMS;

void setup() {
  Serial.begin(115200);
// Initiate the LCD:
  lcd.init();
  lcd.backlight();  
  
  Serial.println("DHT22 test!");

  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);
  
  pinMode(K, INPUT_PULLUP);
  pinMode(P, INPUT_PULLUP);

  pinMode(RELAY_PIN, OUTPUT); 
  digitalWrite(RELAY_PIN, LOW);

 
  // Define um atraso entre as leituras do sensor
  delayMS = sensor.min_delay / 36000;
}

void loop() {
  // Atraso entre as medições
  delay(delayMS);
 
  // Obtém um novo evento de sensores
  sensors_event_t event;

  // Lê a umidade
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Erro na leitura de umidade!"));
  } else {
    Serial.print(F("Umidade: "));
    Serial.print(event.relative_humidity);
    Serial.println(F("%"));

    // Verifica a condição para ligar/desligar a luz
    if (event.relative_humidity < 40.0) {
      digitalWrite(RELAY_PIN, HIGH);  // Liga a luz 
      Serial.println(F("Umidade abaixo de 40%. Luz LED LIGADA."));
    } else {
      digitalWrite(RELAY_PIN, LOW); // Desliga a luz 
      Serial.println(F("Umidade acima ou igual a 40%. Luz LED DESLIGADA."));
    }
  }
  // Mostra a umidade no display
   lcd.setCursor(1, 0); 
    lcd.print("Umid: ");
    lcd.print(event.relative_humidity);
    lcd.print("%");

  delay(1000);

  // Lê a temperatura
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Erro na leitura de temperatura!"));
  } else {
    Serial.print(F("Temperatura: "));
    Serial.print(event.temperature);
    Serial.println(F("°C"));
  }
  //Mostra a temperatura no display    
    lcd.setCursor(1, 1); 
     lcd.print("Temp: ");
     lcd.print(event.temperature);
     lcd.print("°C");

  delay(3000);
  lcd.clear();


  //Funcionamento dos botões para leitura de Fosforo e Potassio
  while (digitalRead(P) == LOW) {
	  Serial.println(F("Fosforo presente"));}
  while (digitalRead(K) == LOW) {
	  Serial.println(F("Potassio presente"));}
 
    // Mostra a presença de fósforo e potássio
    lcd.setCursor(1, 0); 
     lcd.print("Fosforo: ");
    if (digitalRead(P) == LOW)
      lcd.print("Pres.");
    else
      lcd.print("Aus.");

    lcd.setCursor(1, 1);
     lcd.print("Potassio: ");
    if (digitalRead(K) == LOW)
      lcd.print("Pres.");
    else
      lcd.print("Aus."); 

   delay(3000);  
   lcd.clear();
 
      
  // Leitura de pH
    int ldrValue = analogRead(pH);
  Serial.print("pH: ");
  Serial.println(ldrValue); 

  // Mostra a leitura de pH no display
  lcd.setCursor(1, 0); 
     lcd.print("pH: ");
     lcd.print(ldrValue);
     
  delay(3000);

  lcd.clear();
 
  }
