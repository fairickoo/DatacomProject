#include <Servo.h>
unsigned long Data;
Servo myservo;
int incomingByte;
void setup() {
  Serial.begin(115200);
  myservo.attach(9);
  Serial.print("D");
  delay(500);
  //myservo.write(pos);
}
void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == 'r')
    {
      myservo.write(0);
      Serial.print("r");
      delay(500);
    }
    else if (incomingByte == 'm')
    {
      myservo.write(45);
      Serial.print("m");
      delay(500);
      
    }
    else if (incomingByte == 'l')
    {
      myservo.write(90);
      Serial.print("l");
      delay(500);

    }
    else if (incomingByte == '0' || incomingByte == '1' || incomingByte == '2' || incomingByte == '3'
        || incomingByte == '4' || incomingByte == '5')
    {
      Data = incomingByte-'0';
      Serial.print(Data);
      delay(500);
    }
 Data<<=3;


  }
Data<<=4;
  //delay(1000);
}

// Serial.println("ssss");
// delay(5000);
// myservo.write(pos);
/*for (pos = 0; pos <= 45; pos += 1)
  {
  myservo.write(pos);
  delay(15);
  }
  Serial.println(pos);
  delay(1000);
  for (pos = 45; pos <= 90; pos += 1)
  { // goes from 0 degrees to 180 degrees
  // in steps of 1 degree
  myservo.write(pos);
  delay(15);
  }
  Serial.println(pos);
  delay(1000);
  for (pos = 90; pos >= 45; pos -= 1)
  {
  myservo.write(pos);
  delay(15);
  }
  Serial.println(pos);
  delay(1000);
  for (pos = 45; pos >= 0; pos -= 1)
  {
  myservo.write(pos);
  delay(15);
  }
  Serial.println(pos);
  delay(1000);*/
