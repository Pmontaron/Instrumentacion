int intervalo=1000;
int PinSensor = 2; //Sensor conectados en el pin 2
float factorK=7.5;
volatile int NumPulsos;

void ContarPulsos() {
  NumPulsos++;
}

int ObtenerFrecuencia() {
  NumPulsos=0;
  interrupts(); //Habilitamos las interrupciones
  delay(intervalo); //muestra cada 1 segundo
  noInterrupts(); //Deshabilitamos las interrupciones
  return(NumPulsos);
  
}


void setup() {
  Serial.begin(9600); //Salida al monitor del programa
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
}
