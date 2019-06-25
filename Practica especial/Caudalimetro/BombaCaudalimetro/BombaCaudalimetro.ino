//Bomba y caudalímetro
#include <AFMotor.h>

//Motor A
int ENA = 10;
int IN1 = 9;
int IN2 = 8;

//Motor B
int  ENB = 5;
int IN3 = 7;
int IN4 = 6;

int intervalo = 1000; //Intervalo en milisegundos que toma la muestra desde el caudalímetro
int PinSensor = 2; //Sensor conectados en el pin 2
float factorK = 7.5; //Conversión para el caudalímetro S201
volatile int NumPulsos; //Cantidad de pulsos que mide en un determinado tiempo
int VelocidadBomba = 255; //Velocidad a ordenarle a la bomba. Entre 0 y 255




void ContarPulsos() {
  NumPulsos++;
}

int ObtenerFrecuencia() {
  NumPulsos = 0;
  interrupts(); //Habilitamos las interrupciones
  delay(intervalo); //muestra cada 1 segundo
  noInterrupts(); //Deshabilitamos las interrupciones
  return (NumPulsos);
}

void setup() {
  Serial.begin(9600); //Salida al monitor del programa

  //Declaramos todos los pines como salida a las bombas
  pinMode (ENA, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);

  //Declaramos la entrada desde el caudalímetro
  pinMode(PinSensor, INPUT);
  attachInterrupt(digitalPinToInterrupt(PinSensor), ContarPulsos, RISING) ; //(Interrupcion 0(Pin 2), función, Flanco de subida)
}

void loop() {
  float frecuencia = ObtenerFrecuencia() ; //obtenemos la Frecuencia de los pulsos en Hz
  float caudal_L_m = frecuencia / factorK; //calculamos el caudal en L/m
  float caudal_L_h = caudal_L_m * 60; //calculamos el caudal en L/h

  //Enviamos al puerto serie - monitor del Arduino
  Serial.print ("Frecuencia Pulsos: ");
  Serial.print (frecuencia, 0);
  Serial.print("Hz \tCaudal: ");
  Serial.print(caudal_L_m, 3);
  Serial.print(" L/m\t");
  Serial.print(caudal_L_h, 3);
  Serial.println(" L/h   ");

  //Recibimos datos del monitor para variar el caudal que queremos otorgar
  if (Serial.available() > 0) {
    String dato = Serial.readStringUntil('\n');
    VelocidadBomba = dato.toInt();
  }
  
  //MOVER MOTOR A
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW)  ;
  //Variando el próximo valor entre 0 y 255 varía la velocidad
  analogWrite(ENA, VelocidadBomba);

  //MOVER MOTOR B
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW)  ;
  //Variando el próximo valor entre 0 y 255 varía la velocidad
  analogWrite(ENB, 0);
}
