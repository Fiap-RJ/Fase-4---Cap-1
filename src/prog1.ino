#include <DHT.h>
#include <DHT_U.h>
#include "Wire.h"
#include "LiquidCrystal_I2C.h"

const uint8_t DHTPIN = 13;
const uint8_t RELAY_PIN = 19;
const uint8_t PH_PIN = 34;
const uint8_t K_PIN = 12;  // Potássio
const uint8_t P_PIN = 27;  // Fósforo

#define DHTTYPE DHT22

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);

DHT_Unified dht(DHTPIN, DHTTYPE);

unsigned long previousMillis = 0; 
const long interval = 2000;

void setup() {
  Serial.begin(115200);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("FarmTech v4.0");
  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");
  
  dht.begin();
  
  pinMode(K_PIN, INPUT_PULLUP);
  pinMode(P_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  delay(2000);
  lcd.clear();
}

void loop() {
  // 1. Leitura de Umidade e Temperatura (DHT22)
  sensors_event_t event;
  dht.humidity().getEvent(&event);
  
  float umidade = event.relative_humidity;
  
  if (isnan(umidade)) {
    Serial.println(F("Erro na leitura de umidade!"));
  } else {
    // SERIAL PLOTTER
    Serial.println(umidade); 

    // Lógica de irrigação
    if (umidade < 40.0) {
      digitalWrite(RELAY_PIN, HIGH); // Liga a irrigação
    } else {
      digitalWrite(RELAY_PIN, LOW);  // Desliga a irrigação
    }


    lcd.setCursor(0, 0);
    lcd.print("Umid: ");
    lcd.print(umidade, 1);
    lcd.print("% ");
  }

  dht.temperature().getEvent(&event);
  float temperatura = event.temperature;

  if (isnan(temperatura)) {
    Serial.println(F("Erro na leitura de temperatura!"));
  } else {
    lcd.setCursor(0, 1);
    lcd.print("Temp: ");
    lcd.print(temperatura, 1);
    lcd.print((char)223); // Caractere de grau °
    lcd.print("C");
  }

  delay(2000);
  lcd.clear();

  //  Leitura de Nutrientes (Botões)
  bool fosforo_presente = (digitalRead(P_PIN) == LOW);
  bool potassio_presente = (digitalRead(K_PIN) == LOW);

  if (fosforo_presente) Serial.println(F("Fosforo presente"));
  if (potassio_presente) Serial.println(F("Potassio presente"));
  
  lcd.setCursor(0, 0);
  lcd.print("Fosforo: ");
  lcd.print(fosforo_presente ? "PRES" : "AUS ");
  
  lcd.setCursor(0, 1);
  lcd.print("Potassio: ");
  lcd.print(potassio_presente ? "PRES" : "AUS ");

  delay(2000);
  lcd.clear();

  // Leitura de pH (LDR simulando)
  uint16_t ldrValue = analogRead(PH_PIN);
  
  // Mapeamento simples para uma escala de pH (0-14) para demonstração
  // O valor 4095 do ADC será mapeado para 14.
  float phValue = map(ldrValue, 0, 4095, 0, 140) / 10.0;
  
  Serial.print("pH: ");
  Serial.println(phValue);
  
  lcd.setCursor(0, 0);
  lcd.print("pH do Solo:");
  lcd.setCursor(0, 1);
  lcd.print(phValue, 1);
  
  delay(2000);
  lcd.clear();
}