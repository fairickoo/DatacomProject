 if (incomingByte == 'U')
    { if (temp[0] == '\0')
      {
        temp[0] = "U";
        Serial.println("0");
      }
      else if (temp[1] == '\0')
      {
        temp[1] = "U";
        Serial.println("1");
      }
      else
      {
        temp[2] = "U";
        Serial.println("2");
      }
    }

    
    if (incomingByte == 'O')
    { if (temp[0] == "")
      {
        temp[0] = "O";
        Serial.println("0");
      }
      else if (temp[1] == "")
      {
        temp[1] = "O";
        Serial.println("1");
      }
      else
      {
        temp[2] = "O";
        Serial.println("2");
      }
    }

    
    if (incomingByte == 'L')
    { if (temp[0] == "")
      {
        temp[0] = "L";
        Serial.println("0");
      }
      else if (temp[1] == "")
      {
        temp[1] = "L";
        Serial.println("1");
      }
      else
      {
        temp[2] = "L";
        Serial.println("2");
      }
    }

    
    if (incomingByte == 'R')
    { if (temp[0] == "")
      {
        temp[0] = "R";
        Serial.println("0");
      }
      else if (temp[1] == "")
      {
        temp[1] = "R";
        Serial.println("1");
      }
      else
      {
        temp[2] = "R";
        Serial.println("2");
      }
    }

    
    if (incomingByte == 'T')
    { if (temp[0] == "")
      {
        temp[0] = "T";
        Serial.println("0");
      }
      else if (temp[1] == "")
      {
        temp[1] = "T";
        Serial.println("1");
      }
      else
      {
        temp[2] = "T";
        Serial.println("2");
      }
    }

    
    if (incomingByte == 'B')
    { if (temp[0] == "\0")
      {
        temp[0] = "B";
        Serial.println("0");
      }
      else if (temp[1] == "\0")
      {
        temp[1] = "B";
        Serial.println("1");
      }
      else
      {
        temp[2] = "B";
        Serial.println("2");
      }
    }

  }

  #-----------------------------------
  if (incomingByte == 'U')
    { 
        Serial.println("U");
      
    }

    
    if (incomingByte == 'O')
    { Serial.println("O");
    }

    
    if (incomingByte == 'L')
    { Serial.println("L");
    }

    
    if (incomingByte == 'R')
    { Serial.println("R");
    }

    
    if (incomingByte == 'T')
    { Serial.println("T");
    }

    
    if (incomingByte == 'B')
    { Serial.println("B");
    }