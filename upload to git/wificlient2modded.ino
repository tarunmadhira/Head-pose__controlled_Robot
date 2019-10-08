/*
    This sketch sends a string to a TCP server, and prints a one-line response.
    You must run a TCP server in your local network.
    For example, on Linux you can use this command: nc -v -l 3000
*/

#include <ESP8266WiFi.h>`
#include <ESP8266WiFiMulti.h>

#ifndef STASSID
//#define STASSID "JioFi3_A0E253"
//#define STAPSK  "r9446f9vp5"
#define STASSID "T6t"
#define STAPSK  "Tarun1234"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.43.162";
const uint16_t port = 3001;

WiFiClient client;

ESP8266WiFiMulti WiFiMulti;

/* define L298N or L293D motor control pins */
int leftMotorForward = 0;     /* GPIO2(D4) -> IN3   */
int rightMotorForward = 15 ;   /* GPIO15(D8) -> IN1  */
int leftMotorBackward = 2;    /* GPIO0(D3) -> IN4   */
int rightMotorBackward = 13;  /* GPIO13(D7) -> IN2  */


/* define L298N or L293D enable pins */
int rightMotorENB = 12; /* GPIO14(D5) -> Motor-A Enable */
int leftMotorENB = 14;  /* GPIO12(D6) -> Motor-B Enable */

void setup() {
  Serial.begin(115200);

  // We start by connecting to a WiFi network
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(ssid, password);

  Serial.println();
  Serial.println();
  Serial.print("Wait for WiFi... ");

  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(500);

  Serial.print("connecting to ");
  Serial.print(host);
  Serial.print(':');
  Serial.println(port);

  // Use WiFiClient class to create TCP connections
 

  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    Serial.println("wait 5 sec...");
    delay(5000);
    return;
  }

  /* initialize motor control pins as output */
  pinMode(leftMotorForward, OUTPUT);
  pinMode(rightMotorForward, OUTPUT); 
  pinMode(leftMotorBackward, OUTPUT);  
  pinMode(rightMotorBackward, OUTPUT);

  /* initialize motor enable pins as output */
  pinMode(leftMotorENB, OUTPUT); 
  pinMode(rightMotorENB, OUTPUT);
}


void loop() {
  

  // This will send the request to the server


  //read back one line from server
  Serial.println("receiving from remote server");
  String line = client.readStringUntil('\n');
  Serial.println(line);

  //Serial.println("closing connection");
  //client.stop();
  
    /* If the incoming data is "forward", run the "MotorForward" function */
    if (line == "forward") MotorForward();
    /* If the incoming data is "backward", run the "MotorBackward" function */
    else if (line == "backward") MotorBackward();
    /* If the incoming data is "left", run the "TurnLeft" function */
    else if (line == "left") TurnLeft();
    /* If the incoming data is "right", run the "TurnRight" function */
    else if (line == "right") TurnRight();
    /* If the incoming data is "stop", run the "MotorStop" function */
    else MotorStop();
  //Serial.println("wait 1 sec...");
  delay(0.1);
}

void MotorForward(void)   
{
  digitalWrite(leftMotorENB,HIGH);
  digitalWrite(rightMotorENB,HIGH);
  digitalWrite(leftMotorForward,HIGH);
  digitalWrite(rightMotorForward,HIGH);
  digitalWrite(leftMotorBackward,LOW);
  digitalWrite(rightMotorBackward,LOW);
}

/********************************************* BACKWARD *****************************************************/
void MotorBackward(void)   
{
  digitalWrite(leftMotorENB,HIGH);
  digitalWrite(rightMotorENB,HIGH);
  digitalWrite(leftMotorBackward,HIGH);
  digitalWrite(rightMotorBackward,HIGH);
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(rightMotorForward,LOW);
}

/********************************************* TURN LEFT *****************************************************/
void TurnLeft(void)   
{
  digitalWrite(leftMotorENB,HIGH);
  digitalWrite(rightMotorENB,HIGH); 
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(rightMotorForward,HIGH);
  digitalWrite(rightMotorBackward,LOW);
  digitalWrite(leftMotorBackward,LOW);  
}

/********************************************* TURN RIGHT *****************************************************/
void TurnRight(void)   
{
  digitalWrite(leftMotorENB,HIGH);
  digitalWrite(rightMotorENB,HIGH);
  digitalWrite(leftMotorForward,HIGH);
  digitalWrite(rightMotorForward,LOW);
  digitalWrite(rightMotorBackward,LOW);
  digitalWrite(leftMotorBackward,LOW);
}

/********************************************* STOP *****************************************************/
void MotorStop(void)   
{
  digitalWrite(leftMotorENB,LOW);
  digitalWrite(rightMotorENB,LOW);
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(leftMotorBackward,LOW);
  digitalWrite(rightMotorForward,LOW);
  digitalWrite(rightMotorBackward,LOW);
}
