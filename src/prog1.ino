#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 13       // Pino digital ao qual o sensor DHT22 está conectado
#define DHTTYPE DHT22   // Tipo de sensor DHT22

#define RELAY_PIN 19    // Pino digital ao qual o relé está conectado

#define pH 34    // Pino digital no qual o sensor LDR para pH está conectado

#define K 12        // Pino digital para o botao para detecção de Potassio (K)
#define P 27        // Pino digital para o botao para detecção de Fosforo (P)

DHT_Unified dht(DHTPIN, DHTTYPE);

unsigned long delayMS;

void setup() {
  Serial.begin(115200);
  Serial.println("DHT22 test!");

  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);
  
  pinMode(K, INPUT_PULLUP);
  pinMode(P, INPUT_PULLUP);

  pinMode(RELAY_PIN, OUTPUT); // Define o pino do relé como saída
  digitalWrite(RELAY_PIN, LOW); // Garante que o relé esteja desligado (assumindo relé ativo baixo)

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

  // Lê a temperatura
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Erro na leitura de temperatura!"));
  } else {
    Serial.print(F("Temperatura: "));
    Serial.print(event.temperature);
    Serial.println(F("°C"));
  }

 // Leitura de pH
    int ldrValue = analogRead(pH); // Leitura do valor analógico
  Serial.print("pH: ");
  Serial.println(ldrValue); // Mostra no Serial Monitor

  //Funcionamento dos botões para leitura de Fosforo e Potassio
  while (digitalRead(P) == LOW) {
	  Serial.println(F("Fosforo presente"));}
        
  while (digitalRead(K) == LOW) {
	  Serial.println(F("Potassio presente"));} 
  }