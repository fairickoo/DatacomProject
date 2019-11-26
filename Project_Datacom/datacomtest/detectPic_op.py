import cv2 
import serial
import time
import os
import numpy as np

#Edit picture
def Crop(path,pathsave):
    x=60
    y=80
    h=160
    w=160
    img = cv2.imread(path, 0) 
    crop = img[y:y+h, x:x+w]
    cv2.imwrite(pathsave, crop)
def Black_White(path,pathsave):
    img_grey = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    thresh = 64
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite(pathsave, img_binary)
def Resize(path,pathsave):
    img_Trans = cv2.imread(path,0)
    W = 4
    shape=img_Trans.shape
    height, width = shape
    imgScale = W/width
    newX,newY = img_Trans.shape[1]*imgScale, img_Trans.shape[0]*imgScale
    newimg = cv2.resize(img_Trans,(int(newX),int(newY)))
    cv2.imwrite(pathsave, newimg)
def Repicture(path_original,path_crop,path_BW,path_RZ):
    Crop(path_original,path_crop)
    Resize(path_crop,path_RZ)
    Black_White(path_RZ,path_BW)

#get Value
def getValue_pixel(path):
    imV = cv2.imread(path, 0) 
    rows,cols = imV.shape
    for y in range(rows):
        for x in range(cols):
            if imV[y,x]>=128 and imV[y,x]<=255:
                imV[y,x]=1
            else:
                imV[y,x]=0
    #lower
    if ((imV[0][0]==0 and imV[1][1]==0 and imV[2][2]==0 and imV[3][3]==0 and imV[1][0]==0 
    and imV[2][0]==0 and imV[2][1]==0 and imV[3][0]==0 and imV[3][1]==0 and imV[3][2]==0
    and imV[0][1]==1 and imV[1][2]==1 and imV[2][3]==1 )

    or ( imV[1][0]==0  and imV[2][0]==0 and imV[2][1]==0 and imV[3][0]==0 
    and imV[3][1]==0 and imV[3][2]==0 and imV[0][0]==1 and imV[1][1]==1 and imV[2][2]==1 and imV[3][3]==1 ) 

    or (imV[2][0]==0 and imV[3][1]==0 and imV[3][0]==0 and imV[1][0]==1 and imV[2][1]==1 and imV[3][2]==1)

    or (imV[1][0]==0 and imV[2][0]==0 and imV[2][1]==0 and imV[3][0]==0 
    and imV[3][1]==0 and imV[3][2]==0 and imV[0][0]==1 and imV[1][1]==1 and imV[2][2]==0 and imV[3][3]==1 )):
        for y in range(rows):
            for x in range(cols):
                print(imV[y,x], end = '')
            print("\t")
        print('lower')
        return "Lower"
    #upper
    elif ((imV[0][0]==0 and imV[1][1]==0 and imV[2][2]==0 and imV[3][3]==0 and imV[0][1]==0 
    and imV[0][2]==0 and imV[0][3]==0 and imV[1][2]==0 and imV[1][3]==0 and imV[2][3]==0 
    and imV[1][0]==1 and imV[2][1]==1 and imV[3][2]==1)

    or ( imV[0][1]==0  and imV[0][2]==0 and imV[0][3]==0 and imV[1][2]==0 and imV[1][3]==0 
    and imV[2][3]==0 and imV[0][0]==1 and imV[1][1]==1 and imV[2][2]==1 and imV[3][3]==1) 

    or (imV[0][2]==0 and imV[0][3]==0 and imV[1][3]==0 and imV[0][1]==1 and imV[1][2]==1 and imV[2][3]==1 )):
        for y in range(rows):
            for x in range(cols):
                print(imV[y,x], end = '')
            print("\t")
        print('upper')
        return "Upper"
    #left
    elif ((imV[0][0]==0 and imV[1][0]==0 and imV[2][0]==0 and imV[3][0]==0 
    and imV[0][1]==1 and imV[1][1]==1 and imV[2][1]==1 and imV[3][1]==1) 

    or (imV[0][0]==0 and imV[1][0]==0 and imV[2][0]==0 and imV[3][0]==0 
    and imV[0][1]==0 and imV[1][1]==0 and imV[2][1]==0 and imV[3][1]==0 
    and imV[0][2]==1 and imV[1][2]==1 and imV[2][2]==1 and imV[3][2]==1)

    or (imV[1][0]==0 and imV[2][0]==0 and imV[3][0]==0 and imV[0][1]==1 
    and imV[1][1]==1 and imV[2][1]==1 and imV[3][1]==1 )):
        for y in range(rows):
            for x in range(cols):
                print(imV[y,x], end = '')
            print("\t")
        print('left')
        return "Left"
    #right
    elif ((imV[0][2]==0 and imV[1][2]==0 and imV[2][2]==0 and imV[3][2]==0 
    and imV[0][3]==0 and imV[1][3]==0 and imV[2][3]==0 and imV[3][3]==0 
    and imV[0][1]==1 and imV[1][1]==1 and imV[2][1]==1 and imV[3][1]==1 )

    or (imV[0][3]==0 and imV[1][3]==0 and imV[2][3]==0 and imV[3][3]==0 
    and imV[0][2]==1 and imV[1][2]==1 and imV[2][2]==1 and imV[3][2]==1) 

    or (imV[1][3]==0 and imV[2][3]==0 and imV[3][3]==0 and imV[0][2]==1 
    and imV[1][2]==1 and imV[2][2]==1 and imV[3][2]==1  )):
        for y in range(rows):
            for x in range(cols):
                print(imV[y,x], end = '')
            print("\t")
        print('right')
        return "Right"
    #top
    elif ((imV[0][0]==0 and imV[0][1]==0 and imV[0][2]==0 and imV[0][3]==0 
    and imV[1][0]==0 and imV[1][1]==0 and imV[1][2]==0 and imV[1][3]==0
    and imV[2][0]==1 and imV[2][1]==1 and imV[2][2]==1 and imV[2][3]==1 )

    or (imV[0][0]==0 and imV[0][1]==0 and imV[0][2]==0 and imV[0][3]==0 
    and imV[1][0]==1 and imV[1][1]==1 and imV[1][2]==1 and imV[1][3]==1 )): 
        for y in range(rows):
            for x in range(cols):
                print(imV[y,x], end = '')
            print("\t")
        print('top')
        return "Top"
    #bottom
    elif ((imV[2][0]==0 and imV[2][1]==0 and imV[2][2]==0 and imV[2][3]==0 
    and imV[3][0]==0 and imV[3][1]==0 and imV[3][2]==0 and imV[3][3]==0 
    and imV[1][0]==1 and imV[1][1]==1 and imV[1][2]==1 and imV[1][3]==1)

    or (imV[3][0]==0 and imV[3][1]==0 and imV[3][2]==0 and imV[3][3]==0 
    and imV[2][0]==1 and imV[2][1]==1 and imV[2][2]==1 and imV[2][3]==1)): 
        for y in range(rows):
            for x in range(cols):
                print(imV[y,x], end = '')
            print("\t")
        print('bottom') 
        return "Buttom"
    else:
        print('\tRead Error ')
        return 1

#control Arduino and take photo
def Pule():
    while(1): pass
def ReadPicture(lists_pic,comservo):
    print('* status picture')
    path_original = r'C:/out/Pic.bmp'
    path_crop     = r'C:/image/crop/crop.png'
    path_BW       = r'C:/image/b-w/bw.png'
    path_RZ       = r'C:/image/crop/resize/resize.png'
    while(True):
        tempgetV =getValue_pixel(path_BW)
        if tempgetV ==1:
            time.sleep(5)
            print('\tRead new picture')
            Repicture(path_original,path_crop,path_BW,path_RZ)
        elif tempgetV=="Lower":
            lists_pic.append("5")
            comservo.write(b'5')
            break
        elif tempgetV=="Upper":
            lists_pic.append("4")
            comservo.write(b'4')
            break
        elif tempgetV=="Left":
            lists_pic.append("2")
            comservo.write(b'2')
            break
        elif tempgetV=="Right":
            lists_pic.append("3")
            comservo.write(b'3')
            break
        elif tempgetV=="Top":
            lists_pic.append("0")
            comservo.write(b'0')
            break
        elif tempgetV=="Buttom":
            lists_pic.append("1")
            comservo.write(b'1')
            break
        else:
            break
    return lists_pic         
def TakeBegin(comservo):
    lists_pic=[]
    path_original = r'C:/out/Pic.bmp'
    path_crop     = r'C:/image/crop/crop.png'
    path_BW       = r'C:/image/b-w/bw.png'
    path_RZ       = r'C:/image/crop/resize/resize.png'

    while(True):
        if(comservo.inWaiting()):
            raw = comservo.read()
            data = raw.decode('ascii')
            print('---------------------')
            print('Com name       :',comservo.name)
            print('Status arduino :',data)
            print('---------------------')
            #arduino send...
            if data == 'D':
                print('\nServo move Right >')
                comservo.write(b'r')
                raw = comservo.read()
                data = raw.decode('ascii')
                print('status servo : ',data)

                # take photo 0
                print('\n==start camera ==')
                print('statas  : 0 radius')
                os.remove(path_original)
                time.sleep(8)
                Repicture(path_original,path_crop,path_BW,path_RZ)
                print('* Repicture finish')
                ReadPicture(lists_pic,comservo)
                print('Read finish > Temp Picture : ',lists_pic)
                #comservo.write(lists_pic[0])
                if len(lists_pic)==1:
                    print('\nServo move Miduim >')
                    comservo.write(b'm')
                    raw = comservo.read()
                    data = raw.decode('ascii')
                    print('status servo : ',data)

                    # take photo 45
                    print('\n==start camera ==')
                    print('statas  : 45 radius')
                    os.remove(path_original)
                    time.sleep(7)
                    Repicture(path_original,path_crop,path_BW,path_RZ)
                    print('* Repicture finish')
                    ReadPicture(lists_pic,comservo)
                    print('Read finish > Temp Picture : ',lists_pic)
                    #comservo.write(lists_pic[1])
                    if len(lists_pic)==2:
                        print('\nServo move Left >')
                        comservo.write(b'l')
                        raw = comservo.read()
                        data = raw.decode('ascii')
                        print('status servo : ',data)

                        # take photo 90
                        print('\n==start camera ==')
                        print('statas  : 90 radius')
                        os.remove(path_original)
                        time.sleep(7)
                        Repicture(path_original,path_crop,path_BW,path_RZ)
                        print('* Repicture finish')
                        ReadPicture(lists_pic,comservo)
                        print('Read finish > Temp Picture : ',lists_pic)
                        #comservo.write(lists_pic[2])
                        print('------------------------')
                        if len(lists_pic)==3:
                            print('\nComplete ! >')
                            comservo.write(b'C')
                            raw = comservo.read()
                            data = raw.decode('ascii')
                            print('status servo : ',data)
                            Pule()
                            comservo.close()

    return lists_pic
    
#----------------------------------------------------------------
#main 
arduino_servo = serial.Serial('COM17',115200)  
check= TakeBegin(arduino_servo)
