/*----------------------------------------------------------------------
SOFTWARE PER LA COMUNICAZIONE SERIALE TRA SCHEDA ARDUINO E SERVOMOTORI

ARCHETTI IVAN 10/2013
-----------------------------------------------------------------------*/

#include <Servo.h> //Include Servo Library
#include <string.h>
#include <stdlib.h>

//variabili globali
String inputString = "";
int i = 0; //contatore di supporto
int asse = 0;
int pos = 0; //posizione asse 

//Define array of Pins
int servoPin[6] = {6,7,8,9,10,11}; 

//Create array of Servo Object
Servo myservo[6]; 

void setup()
  {
    //settaggio comunicazione seriale
    Serial.begin(9600);
    inputString.reserve(200);
   
    //Attaches the Servo to our object
    for(i = 0; i < sizeof(servoPin)/sizeof(servoPin[0]); i += 1)  
        { 
        myservo[i].attach(servoPin[i]);  
        }    
  }

void loop()
  {
    while (Serial.available()) 
    {
      char inChar = (char)Serial.read(); //leggo la ricezione
      inputString += inChar;  //incremento la stringa letta

      if (inChar == '*')  //scovo il carattere di chiusura messaggio x000* x = asse 000 = angolo * = chiusura messaggio
       {
        asse = estrai_valore(inputString.substring(0,1));
       
        switch (asse)
        {
          case 1:
          pos = estrai_valore(inputString.substring(1,4));
          myservo[0].write(pos);
          break;
      
          case 2:
          pos = estrai_valore(inputString.substring(1,4));
          myservo[1].write(pos); //asseB è gestito da 2 motori
          myservo[2].write(pos);
          break;
          
          case 3:
          pos = estrai_valore(inputString.substring(1,4));
          myservo[3].write(pos);
          break;
          
          case 4:
          pos = estrai_valore(inputString.substring(1,4));
          myservo[4].write(pos);
          break;
          
          case 5:
          pos = estrai_valore(inputString.substring(1,4));
          myservo[5].write(pos);
          break;
         }
       inputString = "";    
      } 
    }
  }



 int estrai_valore(String valore)
   {
    int result = 0;
    char carray[6]; //vettore di supporto
    valore.toCharArray(carray,6); //frammento la stringa in un vettore di caraTteri
    result = atoi(carray); //converto il vettore in intero
    return result; 
   }
  
  
  
