#include <Servo.h>

Servo xservo;
Servo yservo;

int curx = 90;
int cury = 90;
int newx, newy;

boolean stringComplete = false;
String inputString = "";
String cmd="undef";
String param="0";


void setup() {
  xservo.attach(9);
  yservo.attach(10);

  xservo.write(curx);
  yservo.write(cury);
  newx=curx;
  newy=cury;

  Serial.begin(9600);
  inputString.reserve(200);
  Serial.println("Controller initialized");

}

void loop() {
  serialEvent();
  if (stringComplete) {
        cmd=inputString.substring(0, 2);
        param=inputString.substring(2, 5);
        if (cmd=="gy"){
            Serial.println(cury);
        }
        else if (cmd=="gx"){
            Serial.println(curx);
        }
        else if (cmd=="sy"){
            newy=param.toInt();
        }
        else if (cmd=="sx"){
            newx=param.toInt();
        }
        else if (cmd=="test"){
           Serial.println("OK");
        }
        else{
            Serial.println("commands: gx,gy,sx***,sy***");
        }
   
        //Debug
        if (1==2){
          Serial.println("cmd "+cmd);
          Serial.println(param);
          Serial.println(newx);
          Serial.println(newy);
        }
        if (newx != curx){
          xservo.write(newx);
          curx=newx;
        }
        if (newy != cury){
          yservo.write(newy);
          cury=newy;
        }
        cmd="undef";
        param="0";
        inputString = "";
        stringComplete = false; 
  }
}



void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
