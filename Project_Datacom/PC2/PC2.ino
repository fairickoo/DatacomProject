#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

#include <Wire.h>
#include <Adafruit_MCP4725.h>
#include <Adafruit_ADS1015.h>
Adafruit_MCP4725 dac;

#include <Servo.h>
Servo myservo;
//int incomingByte;

/******************************************************************************FSK******************************************************************************************/

#define r_slope 80

#define frequency0 500
#define frequency1 750
#define frequency2 1000
#define frequency3 1250

#define delay0 1411/4
#define delay1 711/4
#define delay2 411/4
#define delay3 211/4

#define IFrame 0
#define SFrame 2
#define UFrame 3

const uint16_t S_DAC[4] = {2047, 4095, 2047, 0};
int baudRate = 250;
int prev = 0;
int check = false;
int check2 = false;
int count = 0;
uint32_t startFreq = 0;
uint8_t bitC = 0; //จำนวน 2*(bit หรือ Frame) ที่ได้รับ
int period = 3800; //คาบ FSK

/************************************************************************************ตัวแปรสัพเพเหระ*****************************************************************************************/

unsigned long timedOut = 5500, clockTime = 0, startTime = 0; //ตัวจับเวลา TimeOut
unsigned long int outFrame = 0, inFrame = 0; //Frame ที่จะส่ง และรับเข้ามา
int frameNo = 0, ackNo = 0; //หมายเลข Frame และ ACK
char type = 'X'; //ประเภทของเฟรม
unsigned long Data = 0; //ข้อมูล
boolean startTimer = false;
boolean once = true;
int store[3];

/************************************************************************************ S E T U P ********************************************************************************************/

void setup() {
  sbi(ADCSRA, ADPS2);
  cbi(ADCSRA, ADPS1);
  cbi(ADCSRA, ADPS0);
  dac.begin(0x62);
  Serial.begin(115200);
  myservo.attach(9);
  Serial.flush();
}

/************************************************************************************ L O O P *****************************************************************************************/

void loop() {
  receiveFrame();
  if (startTimer)
  {
    clockTime = millis();
    if (clockTime - startTime > timedOut)
    {
      //Serial.println("...Retransmitting Frame...");
      sendFrame(false);
    }
  }
  else {
    clockTime = 0;
  }
}

/************************************************************************* c h e c k F r a m e( ) *****************************************************************************************/

void checkFrame() //สำหรับเช็คเฟรมที่รับเข้ามา
{
  //  Serial.print("R:");
  //    Serial.print(inFrame, BIN);
  if (checkError(inFrame)) //Check Error ของเฟรมที่รับเข้ามา โดยใช้ CRC
  {
    //    Serial.println("!E");
    if (inFrame >> 10 == UFrame) //ข้อมูลที่รับเข้ามาเป็น U-Frame
    {
      int temp = (inFrame >> 5)&B11111;
      //Serial.println("...Accepting Request...");
      Data = 0x6000;
      type = 'U';
      sendFrame(true); //ตอบ ACK แบบไม่จับเวลา
      if (temp == B11100) //Code สำหรับเริ่มการทำงาน
      {
        //Serial.println("CC");
        //Serial.println("--------------------------------------------");
      }
      else if (temp == B00110) //Code สำหรับจบการทำงาน
      {
        //Serial.println("TC");
        //Serial.println("--------------------------------------------");
      }
    }
    else if (inFrame >> 10 == IFrame) //ข้อมูลที่รับเข้ามาเป็น I-Frame
    {
      //Serial.println("--------------------------------------------");
      //Serial.println("SK");
      type = 'S'; //S-Frame สำหรับตอบ ACK
      Data = 0x8000;
      delay(500);
      sendFrame(true); //ตอบ ACK แบบไม่จับเวลา
      //      Serial.println(outFrame, BIN);
      delay(1000);
      int temp = (inFrame >> 9) & 1 ;
      if (temp == ackNo) //ถ้าหมายเลข Frame ที่รับมาตรงกับหมายเลข ACK ที่รอรับอยู่
      {
        if (ackNo) ackNo = 0; //สลับเลข ACK
        else ackNo = 1;
        int tempo = (inFrame >> 6) & B111;
        Data = 0;
        if (tempo == B111) //ถ้าได้รับคำสั่งให้ Scan ทุกรูป
        {
          scanall();
          //Data = 0xB18C;
        }
        else //ถ้าได้รับคำสั่งอื่น (ถ่ายรูปเดี่ยวๆ)
        {
          myservo.write(indexof(tempo));
          delay(500);
          switch (tempo)
          {
            case B000: //Top
              Serial.print('T');
              delay(500);
              break;
            case B001: //Bottom
              Serial.print('B');
              delay(500);
              break;
            case B010: //Left
              Serial.print('L');
              delay(500);
              break;
            case B011: //Right
              Serial.print('R');
              delay(500);
              break;
            case B100: //Upper
              Serial.print('U');
              delay(500);
              break;
            default: //Lower
              Serial.print('O');
              delay(500);
              break;
          }
          if (Serial.available() > 0)
          {
            for (int i = 0; i < 16; i++)
            {
              Data |= Serial.read();
              Data <<= 1;
            }
          }
          Data >>= 1;
        }
        type = 'I';

        //        Serial.print(Data);
        sendFrame(false);
      }
    }
    else if (inFrame >> 10 == SFrame) //ข้อมูลที่รับเข้ามาเป็น S-Frame
    {
      //Serial.println("--------------------------------------------");
      //Serial.println("RK");
      startTimer = false;
      frameNo = inFrame & 1; //เปลี่ยนหมายเลข Frame ให้ตรงกับ หมายเลข ACK ที่รับเข้ามา
    }
  }
  else
  {
    //    Serial.println("E");
  }

}

void scanall()
{
  int j = 0;
  Serial.flush();
  Serial.print("D");
  delay(500);
  int incomingByte;
  if (Serial.available() > 0) {
    //scanall()
    do {
      incomingByte = Serial.read();
      if (incomingByte == 'r')
      {
        myservo.write(0);
        Serial.flush();
        Serial.print("r");
        delay(200);
      }
      else if (incomingByte == 'm')
      {
        myservo.write(45);
        Serial.flush();
        Serial.print("m");
        delay(200);

      }
      else if (incomingByte == 'l')
      {
        myservo.write(90);
        Serial.flush();
        Serial.print("l");
        delay(200);
      }
      else if (incomingByte == '0' || incomingByte == '1' || incomingByte == '2' || incomingByte == '3'
               || incomingByte == '4' || incomingByte == '5')
      {
        Data |= incomingByte - '0';
        Data <<= 3;
        Serial.print(Data);
        store[j] = incomingByte - '0';
        j++;
        delay(500);
      }
    }
    while (incomingByte != 'C');
    //    myservo.write(0);
    //    delay(500);
    Data <<= 4;
  }

}
/************************************************************************ r e c i v e F r a m e( ) ****************************************************************************************/

void receiveFrame()
{ //Serial.println("--------------receiveFrame function ");
  int tmp = analogRead(A0);
  if (tmp > r_slope && prev < r_slope && check == false) {
    check = true;
    if (check2 == false) {
      startFreq = micros();
    }
  }
  if (tmp < r_slope && check2 == true) {
    if (micros() - startFreq > period) { //นับเป็นคาบ
      inFrame >>= 2;
      int temp = (count - 2) & B0011;
      temp *= 0x400; //สลับ bit ของข้อมูลที่รับมา
      inFrame |= temp;
      bitC++;
      if (bitC == 6) { //เมื่อได้รับครบ 12 bit
        checkFrame(); //เช็ค Frame ที่รับเข้ามา
        inFrame = 0;
        bitC = 0;
      }
      check2 = false;
      count = 0;
    }
  }
  if (tmp > 255 - r_slope && check == true) { //นับจำนวนลูกคลื่น
    count++;
    check2 = true;
    check = false;
  }
  prev = tmp;
}

/****************************************************************************** C R C **************************************************************************************************/

void CRC() //เอา Data มาต่อ CRC
{
  if (outFrame != 0)
  {
    unsigned long canXOR = 0x8000000;//ตั้งใหญ่ๆไว้ก่อนเพื่อเอามาเช็คขนาดดาต้า
    unsigned long remainder = outFrame << 5;//ตัวแปรใหม่ที่มาจากการเติม 0 หลัง outFrame 5 ตัว
    unsigned long divisor = B110101;//กำหนด divisor
    unsigned long tmp = canXOR & remainder;//ไว้ตรวจว่าจะเอา remainder ไป or ตรงไหนใน data(ต้อง XOR ตัวหน้าสุดก่อน)
    while (tmp == 0)
    {
      canXOR >>= 1;//ปรับขนาดให้เท่ากับดาต้า
      tmp = canXOR & remainder;
    }
    tmp = canXOR & divisor;//ไว้ตรวจว่าจะเริ่ม XOR ตำแหน่งไหน
    while (tmp == 0)
    {
      divisor <<= 1;//ชิพไปเรื่อยๆจนกว่าจะถึงตำแหน่ง XOR แรก
      tmp = canXOR & divisor;
    }
    while (divisor >= B110101)//ทำจนกว่า divisor จะน้อยกว่าค่าที่กำหนด
    {
      tmp = remainder & canXOR;//ดูว่าตำแหน่งนี้ XOR ได้หรือไม่(XOR ตำแหน่งที่เป็น 1xxxxx)
      if (tmp > 0)remainder = remainder ^ divisor;//ทำการ XOR
      divisor >>= 1;
      canXOR >>= 1;
    }
    outFrame <<= 5;//เติม0 5ตัว
    outFrame += remainder;//เปลี่ยน5บิตสุดท้ายเป็นremainder
  }
}

/************************************************************************* c h e c k E r r o r ( ) *****************************************************************************************/

boolean checkError(unsigned long data) //ใช้ CRC เช็ค Error
{
  if (data != 0)
  {
    unsigned long canXOR = 0x8000000;
    unsigned long remainder = data;
    unsigned long divisor = B110101;
    unsigned long tmp = canXOR & remainder;
    while (tmp == 0)
    {
      canXOR >>= 1;
      tmp = canXOR & remainder;
    }

    tmp = canXOR & divisor;
    while (tmp == 0)
    {
      divisor <<= 1;
      tmp = canXOR & divisor;
    }
    while (divisor >= B110101)
    {
      tmp = remainder & canXOR;
      if (tmp > 0)remainder = remainder ^ divisor;
      divisor >>= 1;
      canXOR >>= 1;
    }
    if (remainder == 0)return true;//ถ้าเศษเป็น0 return true
    else return false;//ถ้าไม่ return false
  }
}

/************************************************************************* m a k e F r a m e( ) *****************************************************************************************/

void makeFrame() //สร้างเฟรมที่จะส่ง
{
  outFrame = 0; //Reset
  switch (type)
  {
    case 'I': //I-Frame [00|1|0101010101010101] = [ประเภทเฟรม|หมายเลข Frame|ข้อมูล]
      outFrame = IFrame;
      outFrame <<= 1;
      outFrame |= frameNo;
      outFrame <<= 16;
      outFrame |= Data;
      break;
    case 'S': //S-Frame [10|10000000000000000|1] = [ประเภทเฟรม|ประเภทการทำงาน|หมายเลข ACK]
      outFrame = SFrame;
      outFrame <<= 16;
      outFrame |= Data;
      outFrame <<= 1;
      outFrame |= ackNo;
      break;
    default: //U-Frame [11|10101010101010101] = [ประเภทเฟรม|ประเภทการทำงาน]
      outFrame = UFrame;
      outFrame <<= 17;
      outFrame |= Data;
      break;
  }
}

/************************************************************************* s e n d F r a m e( ) *****************************************************************************************/

void sendFrame(boolean isAck) //สำหรับส่งข้อมูล
{
  makeFrame(); //สร้าง Frame
  CRC(); //เอาข้อมูลที่จะส่งมาต่อด้วย CRC
  //  Serial.print("S:");
  //    Serial.println(outFrame, BIN);
  if (!isAck) //ถ้าไม่ใช่ ACK ให้จับเวลา
  {
    startTime = clockTime;
    startTimer = true;
  }
  for (int k = 23 ; k >= 0 ; k -= 2) { //วนส่งทีละ 2 bit จาก 24 bit
    int tmp = outFrame & 3;
    switch (tmp)
    {
      case 0: //00
        sendFSK(frequency0, delay0);
        break;
      case 1: //01
        sendFSK(frequency1, delay1);
        break;
      case 2: //10
        sendFSK(frequency2, delay2);
        break;
      default: //11
        sendFSK(frequency3, delay3);
        break;
    }
    outFrame >>= 2;
  }
  dac.setVoltage(0, false); //เมื่อไม่ได้มีการส่งข้อมูล
}

/************************************************************************* s e n d F S K ( ) *****************************************************************************************/

void sendFSK(int frequency, int delayTime) //FSK Modulation
{
  for (int m = 0; m < frequency / baudRate; m++) {
    for (int j = 0 ; j < 4; j++) {
      dac.setVoltage(S_DAC[j], false);
      delayMicroseconds(delayTime);
    }
  }
}

int indexof(int data)
{
  for (int i = 0; i < sizeof(store); i++)
  {
    if (store[i] == data)
    {
      return i * (45);
    }
  }
}
