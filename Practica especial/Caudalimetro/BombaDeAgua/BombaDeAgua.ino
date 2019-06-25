#include <AFMotor.h>

//Motor A
int ENA = 10;
int IN1 = 9;
int IN2 = 8;

//Motor B
int  ENB = 5;
int IN3 = 7;
int IN4 = 6;

void setup() {
  //Declaramos todos los pines como salida
  pinMode (ENA, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);
}

void loop() {
  //MOVER MOTOR A
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW)  ;
  //Variando el próximo valor entre 0 y 255 varía la velocidad
  analogWrite(ENA, 180);

  //MOVER MOTOR B
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW)  ;
  //Variando el próximo valor entre 0 y 255 varía la velocidad
  analogWrite(ENB, 255);
}
