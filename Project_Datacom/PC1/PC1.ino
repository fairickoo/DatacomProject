#include <Wire.h>
#include <Adafruit_MCP4725.h>
#include <Adafruit_ADS1015.h>
Adafruit_MCP4725 dac;

#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

/********************************************FSK********************************************/

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
uint32_t startFreq = 0;
int baudRate = 250;
int prev = 0;
int check = false;
int check2 = false;
int count = 0;
int pixels[48];
int period = 3800; //จำนวนคาบของ FSK
uint8_t bitC = 0; //จำนวน 2*(bit หรือ Frame) ที่ส่ง

/********************************************ตัวแปรสัพเพเหระ********************************************/
int state = 0;

unsigned long timedOut = 7000, clockTime = 0, startTime = 0; //ตัวจับเวลา TimeOut
unsigned long int outFrame = 0, inFrame = 0; //Frame ที่จะส่ง และรับเข้ามา
String function; //สำหรับเลือก function
int frameNo = 0, ackNo = 0; //หมายเลข Frame และ ACK
char type = 'X'; //ประเภทของเฟรม I, S และ U
int Data = 0; //Data ที่ส่ง
int pixelCount = 0;
boolean startConnection = true, canSend = true, isScan = true; //State การทำงาน (อย่าลืมแก้กลับ)
boolean startTimer = false; //
void setup() {
  Serial.begin(115200);
  dac.begin(0x62);
  sbi(ADCSRA, ADPS2);
  cbi(ADCSRA, ADPS1);
  cbi(ADCSRA, ADPS0);
}

void loop() {
  receiveFrame(); //รับเฟรม

  if (Serial.available() > 0 and canSend) //ถ้าส่งได้
  {
    function = Serial.readString(); //อ่านฟังก์ชันที่จะทำ
    Serial.println(function);
    if (startConnection && function.equalsIgnoreCase("start")) //เมื่อเริ่มการทำงานครั้งแรก
    {
      Serial.println("....Connecting....");
      Data = B11100;
      type = 'U'; //U-Frame สำหรับเริ่มการติดต่อ
      sendFrame(false); //ส่งแบบจับ TimeOut
      startConnection = false;
    }
    else
    {
      if (state == 0 && function.equalsIgnoreCase("scanall") || function.equalsIgnoreCase("Scan all") || function.equalsIgnoreCase("scan") || function.equalsIgnoreCase("sc"))
      {
        Data = B1110;
        state = 1;
      }
      else if (state == 1)
      {
        if (function.equalsIgnoreCase("top") || function.equalsIgnoreCase("t"))
        {
          Data = B0000;
        }
        else if (function.equalsIgnoreCase("bottom") || function.equalsIgnoreCase("b"))
        {
          Data = B0010;
        }
        else if (function.equalsIgnoreCase("left") || function.equalsIgnoreCase("l"))
        {
          Data = B0100;
        }
        else if (function.equalsIgnoreCase("right") || function.equalsIgnoreCase("r"))
        {
          Data = B0110;
        }
        else if (function.equalsIgnoreCase("upper") || function.equalsIgnoreCase("u"))
        {
          Data = B1000;
        }
        else if (function.equalsIgnoreCase("lower") || function.equalsIgnoreCase("o") || function.equalsIgnoreCase("lo"))
        {
          Data = B1010;
        }
      }
      type = 'I'; //I-Frame สำหรับส่งข้อมูล
      sendFrame(false); //ส่งแบบจับ TimeOut
      canSend = false;
    }
  }

  if (startTimer) //เมื่อมีการจับเวลา
  {
    clockTime = millis();
    if (clockTime - startTime > timedOut) //เมื่อเวลา TimeOut ส่งเฟรมใหม่
    {
      Serial.println("...Retransmitting Frame...");
      sendFrame(false); //ส่งแบบจับ TimeOut
    }
  }
  else clockTime = 0;

}
void makeFrame() //สำหรับสร้างเฟรม
{
  outFrame = 0; //Reset Frame ที่จะส่ง
  switch (type)
  {
    case 'I': //I-Frame [00|1|0010] = [ประเภทเฟรม|หมายเลข Frame|ข้อมูล]
      outFrame = IFrame;
      outFrame <<= 1;
      outFrame |= frameNo;
      outFrame <<= 4;
      outFrame |= Data;
      break;
    case 'S': //S-Frame [10|1000|1] = [ประเภทเฟรม|ประเภทการทำงาน|หมายเลข ACK]
      outFrame = SFrame;
      outFrame <<= 4;
      outFrame |= Data;
      outFrame <<= 1;
      outFrame |= ackNo;
      break;
    default: //U-Frame [11|00101] = [ประเภทเฟรม|ประเภทการทำงาน]
      outFrame = UFrame;
      outFrame <<= 5;
      outFrame |= Data;
      break;
  }
}
void sendFrame(boolean isAck) //สำหรับส่งเฟรม
{
  makeFrame(); //สร้างเฟรมที่จะส่ง
  CRC(); //เอาเฟรมที่จะส่งมาต่อด้วย CRC
  Serial.print("Sending: ");
  Serial.println(outFrame, BIN);
  if (!isAck) //ถ้าไม่เป็น ACK ให้จับเวลา
  {
    startTime = clockTime;
    startTimer = true;
  }
  for (int k = 11 ; k >= 0 ; k -= 2) { //วนส่งที่ละ 2 bit Data ที่จะส่งมี 12 bit มากสุด (รวม CRC)
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
  dac.setVoltage(0, false); //เมื่อไม่ส่ง Data
}
void sendFSK(int frequency, int delayTime) //FSK Modulation
{
  for (int m = 0; m < frequency / baudRate; m++) {
    for (int j = 0 ; j < 4; j++) {
      dac.setVoltage(S_DAC[j], false);
      delayMicroseconds(delayTime);
    }
  }
}
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
void receiveFrame() //สำหรับรับเฟรม
{
  int tmp = analogRead(A0);
  if (tmp > r_slope && prev < r_slope && check == false) {
    check = true;
    if (check2 == false) {
      startFreq = micros();
    }
  }
  if (tmp < r_slope && check2 == true) {
    if (micros() - startFreq > period) {
      inFrame >>= 2;
      unsigned long temp = (count - 2) & 3;
      //      Serial.println(temp);
      temp *= 0x10000; //กลับ bit ของข้อมูล
      inFrame |= temp;
      bitC++;
      if (bitC == 9) { //เมื่อรับครบทุก bit แล้ว
        checkFrame(); //เช็คว่า เฟรมที่รับมาเป็นอะไร
        inFrame = 0; //Reset
        bitC = 0;
      }
      check2 = false;
      count = 0;
    }
  }
  if (tmp > 255 - r_slope && check == true) {
    count++;
    check2 = true;
    check = false;
  }
  prev = tmp;
}
void checkFrame()
{
  Serial.print("Received frame: ");
  Serial.print(inFrame, BIN);
  if (checkError(inFrame)) { //เช็ค Error ของข้อมูลที่ได้รับมา
    Serial.println(" -> is not Error.");
    if (inFrame >> 16 == UFrame) //ถ้าเป็น U-Frame
    {
      int tmp = inFrame >> 11 & B11111;
      if (tmp == B00110) //ACK เมื่อตอบรับการเชื่อมต่อ หรือหยุดการทำงาน
      {
        startTimer = false;
        if (state == 0) {
          Serial.println("Connection compleated.");
          Serial.println("---------------------------------------------------");
          Serial.print("Please type scanall first: ");
          canSend = true;
        }
        else {
          state = 2;
          Serial.println("Termination compleated.");
          Serial.println("---------------------------------------------------");
        }
      }
    }
    else if (inFrame >> 16 == IFrame) //ถ้าเป็น I-Frame
    {
      Serial.println("---------------------------------------------------");
      Serial.println("...Sending ACK...");
      type = 'S'; //S-Frame สำหรับตอบ ACK
      Data = 0x8;
      delay(500);
      sendFrame(true); //ตอบ ACK กลับ แบบไม่จับเวลา
      delay(1000);
      int temp = (inFrame >> 15) & 1;
      //      Serial.println(temp);
      //      Serial.print("ACK");
      //      Serial.println(ackNo);
      if (temp == ackNo) //เมื่อหมายเลข Frame ที่ได้รับมาตรงกับ หมายเลข ACK ที่รอรับอยู่
      {
        //        Serial.println("bh");
        if (ackNo)ackNo = 0; //สำหรับเลข ACK
        else ackNo = 1;
        //        Serial.println(isScan);
        if (isScan) //ให้นำข้อมูลที่แสกนมา มา Display
        {
          Serial.println("---------------------------------------------------");
          Serial.print("Display: ");
          list(((inFrame >> 6) & 0x1FF) >> 6);
          Serial.print("at 45 degrees , ");
          list((((inFrame >> 6) & 0x1FF) >> 3)&B111);
          Serial.print("at 0 degrees , ");
          list((((inFrame >> 6) & 0x1FF))&B111);
          Serial.println("at -45 degrees.");
          Serial.print("Please choose a picture: ");
          isScan = false;
          canSend = true;
        }
        else //เมื่อได้รับข้อมูลภาพมา
        {
          Serial.println("---------------------------------------------------");
          Serial.print("...Receiving Pixels No.");
          Serial.print(pixelCount);
          Serial.print(": ");
          Serial.print((inFrame >> 7) & 0xFF);
          Serial.println("...");
          pixels[pixelCount] = (inFrame >> 7) & 0xFF;
          pixelCount++;
          if (pixelCount == 48)
          {
            Serial.println("...Displaying Image...");
            Display();
            type = 'U';
            Data = B00110;
            Serial.println("...Terminating..."); //จบการทำงาน
            sendFrame(false); //ส่งแบบจับ TimeOut
            delay(500);
          }
        }
      }
    }
    else if (inFrame >> 16 == SFrame) //ถ้าเป็น S-Frame
    {
      Serial.println("---------------------------------------------------");
      Serial.println("...Receiving ACK...");
      frameNo = inFrame & 1; //เปลี่ยนเลข Frame ที่จะส่งตามหมายเลข ACK ที่รับมา
      startTimer = false;
    }
  }
  else
  {
    Serial.println(" -> is Error.");
  }
}
void list(unsigned long tempo) //map ค่าที่รับมาเป็นคำ
{
  if     (tempo == B000)Serial.print("Top ");
  else if (tempo == B001)Serial.print("Bottom ");
  else if (tempo == B010)Serial.print("Left ");
  else if (tempo == B011)Serial.print("Right ");
  else if (tempo == B100)Serial.print("Upper ");
  else if (tempo == B101)Serial.print("Lower ");
}
void Display()
{
  Serial.print('\t');
  for (int x = 0; x < 12; x += 3)
  {
    Serial.print(pixels[x]);
    Serial.print('\t');
  }
  for (int i = 0; i < 48; i++)
  {
    if (i % 12 == 1)
    {
      Serial.println("\n");
      Serial.print(pixels[i]);
      Serial.print('\t');
    }
    if (i % 3 == 2)
    {
      Serial.print(pixels[i]);
      Serial.print('\t');
    }

  }
  Serial.println();
}
