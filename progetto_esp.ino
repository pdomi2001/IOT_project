#define DHTTYPE DHT11   // DHT 11
#define dht_dpin 5
DHT dht(dht_dpin, DHTTYPE); 

#include <ArduinoMqttClient.h>
#include "arduino_secrets.h"

// costanti
char ssid[]  = SECRET_SSID;   // your network SSID (name)
char pass[]  = SECRET_PASS;   // your network password

float h_stanza = 0.0;
float t_stanza = 0.0;   

float t_termosifone = 0.0;

DS18B20 ds(14);

char clientID[]  = "iot_paride_1";

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[]      = "192.168.0.10";
IPAddress broker_ip(192, 168, 0, 10);
int        port          = 1883;
const char topic[]       = "iot/message";
const char topic_sync[]  = "iot/sync";
const char listenTopic[] = "iot/led";

int count = 0;
int count_wifi_connections = 0;
int count_mqtt_connections = 0;

void setup() {
  Serial.begin(115200);
  Serial.println();
  
  Connect2WiFi();
  
  // metto una pausa per dare il tempo al wifi di stabilizzarsi
  delay(5000);

  Connect2MQTT();

  dht.begin();

}

void loop() {
  Serial.println("---- inizio loop ----");
  // Se il wifi si è sconnesso lo riconnetto
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi down - Reconnecting");
    Connect2WiFi();
  }
  ReadSensors();
  delay(2000);
  // Se il client mqtt si è sconnesso lo riconnetto
  if (!mqttClient.connected()) {
    Serial.println("MQTT down - Reconnecting");
    Connect2MQTT();
  }
  writeToMQTT();
  // writeToInfluxDB();
  
  Serial.println("---- fine loop ----");
  delay(30000);
}

void Connect2WiFi() {
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }
  //WiFi.setOutputPower(20.5);
  WiFi.setTxPower(WIFI_POWER_19_5dBm); //ESP32

  Serial.println("You're connected to the network");
  count_wifi_connections++;

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
}


void Connect2MQTT() {
  // Each client must have a unique client ID
  mqttClient.setId(clientID);
  bool ok = false;
//  if (!mqttClient.connect(broker, port)) {
  while (!ok) {
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("WiFi down - Reconnecting");
      Connect2WiFi();
    }
    Serial.print("Attempting to connect to the MQTT broker: ");
    Serial.println(broker);
    Serial.print("Attempting to connect to the MQTT port: ");
    Serial.println(port);
    if (!mqttClient.connect(broker_ip, port)) {
      Serial.print("MQTT connection failed! Error code = ");
      Serial.println(mqttClient.connectError());
      delay(5000);
    } else {
      ok = true;
      count_mqtt_connections++;
    }
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
  // set the message receive callback
  mqttClient.onMessage(onMqttMessage);

  Serial.print("Subscribing to topic: ");
  Serial.println(listenTopic);
  Serial.println();

  // subscribe to a topic
  mqttClient.subscribe(listenTopic);
}

void writeToMQTT() {
  // call poll() regularly to allow the library to send MQTT keep alives which
  // avoids being disconnected by the broker
  mqttClient.poll();

  Serial.print("Sending message to topic: ");
  Serial.println(topic);
  Serial.print("hello ");
  Serial.println(count);

  // send message, the Print interface can be used to set the message contents
  mqttClient.beginMessage(topic);


  mqttClient.print("sender_ip=");
  mqttClient.print(WiFi.localIP());
  mqttClient.print(";clientID=");
  mqttClient.print(clientID);
  mqttClient.print(";h_stanza=");
  mqttClient.print(h_stanza);
  mqttClient.print(";t_stanza=");
  mqttClient.print(t_stanza);
  mqttClient.print(";t_termosifone=");
  mqttClient.print(t_termosifone);
  mqttClient.print(";count=");
  mqttClient.print(count);
  mqttClient.print(";count_wifi_c=");
  mqttClient.print(count_wifi_connections);
  mqttClient.print(";count_mqtt_c=");
  mqttClient.print(count_mqtt_connections);
  
  mqttClient.endMessage();

  Serial.println();
  count++;
}

void ReadSensors() {
  Serial.println(WiFi.localIP());

  h_stanza = dht.readHumidity();
  t_stanza = dht.readTemperature();   
  
  t_termosifone = ds.getTempC();
  if (isnan(h_stanza) || isnan(t_stanza)) 
  {
    Serial.println("Failed to read from DHT sensor!");
  }

  Serial.println( "Temperature value " + String( t_stanza ) );
  Serial.println( "Humidity value " + String( h_stanza ) );

  Serial.println( "Sensore DS18B20" );
  Serial.println( "Temperature value " + String( t_termosifone ) );

}

void onMqttMessage(int messageSize) {
  // we received a message, print out the topic and contents
  Serial.println("Received a message with topic '");
  Serial.print(mqttClient.messageTopic());
  Serial.print("', length ");
  Serial.print(messageSize);
  Serial.println(" bytes:");

  char msg[messageSize];
  int i = 0;

  // use the Stream interface to print the contents
  while (i < messageSize && mqttClient.available()) {
    msg[i] = (char)mqttClient.read();    
    i++;
  }
  String msgString = String(msg).substring(0,messageSize);
  Serial.print("received message ");
  Serial.println(msgString);
}