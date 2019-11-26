import cv2 
import serial
import time
import os
import numpy as np
def Crop(x,y,h,w,path,pathsave) :
    img = cv2.imread(path, 0) 
    crop = img[y:y+h, x:x+w]
    #cv2.imshow('Image crop',crop)
    cv2.imwrite(pathsave, crop)

def Black_White(path,pathsaveBW):
    img_grey = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    thresh = 64
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow('Image crop',img_binary)
    cv2.imwrite(pathsaveBW, img_binary)

def Resize(path,pathsave):
    img_Trans = cv2.imread(path,0)
    W = 4
    shape=img_Trans.shape
    height, width = shape
    imgScale = W/width
    newX,newY = img_Trans.shape[1]*imgScale, img_Trans.shape[0]*imgScale
    newimg = cv2.resize(img_Trans,(int(newX),int(newY)))
    #cv2.imshow("Show by CV2",newimg)
    cv2.imwrite(pathsave, newimg)
    
def getValue_pixel(path):
    imV = cv2.imread(path, 0) 
    #p = imV.shape
    rows,cols = imV.shape
    for y in range(rows):
        for x in range(cols):
            if imV[y,x]>=128 and imV[y,x]<=255:
                imV[y,x]=1
            else:
                imV[y,x]=0
            #print(imV[y,x], end = '')
        #print("\t")
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
        print('===error===')
        for y in range(rows):
            for x in range(cols):
                print(imV[y,x], end = '')
            print("\t")
        print('--------------') 
        return 1
            
            
    #print('W H :',p)
    #cv2.imshow('Imagefor get value =',imgV)

def Pule():
    while(1): pass


def TakeBegin(comservo):
    lists=[]
    path_original = r'C:/out/Pic.bmp'
    path_crop=r'C:/image/crop/test.png'
    path_BW=r'C:/image/b-w/bw.png'
    path_RZ= r'C:/image/crop/resize/h.png'
    while(True):
        if(comservo.inWaiting()):
            raw = comservo.read()
            data = raw.decode('ascii')
            print('Com name :',comservo.name)
            print('Status arduino :',data)
            print('\n-------------')
            if data== 'D':
                x=60
                y=80
                h=160
                w=160
                comservo.write(b'r')
                print('hee')
                raw = comservo.read()
                data = raw.decode('ascii')
                print('servo reply : ',data)
                #r
                os.remove(path_original)
                time.sleep(7)
                Crop(x,y,h,w,path_original,path_crop)
                print('crop')
                Resize(path_crop,path_RZ)
                print('resize')
                Black_White(path_RZ,path_BW)
                print('bw')
                while (1):
                    print('while')
                    tempgetV =getValue_pixel(path_BW)
                    if tempgetV ==1:
                        time.sleep(5)
                        print('===new pic path 1===')
                        path_original = r'C:/out/Pic.bmp'
                        Crop(x,y,h,w,path_original,path_crop)
                        Resize(path_crop,path_RZ)
                        Black_White(path_RZ,path_BW)
                        #getValue_pixel(path_BW)
                        print('---------------')
                    elif tempgetV=="Lower":
                        print('lower_GV')
                        lists.append('O')
                        break
                    elif tempgetV=="Upper":
                        print('upper_GV')
                        lists.append('U')
                        break
                    elif tempgetV=="Left":
                        print('left_GV')
                        lists.append('L')
                        break
                    elif tempgetV=="Right":
                        print('right_GV')
                        lists.append('R')
                        break
                    elif tempgetV=="Top":
                        print('top_GV')
                        lists.append('T')
                        break
                    elif tempgetV=="Buttom":
                        print('bottom_GV')
                        lists.append('B')
                        break
                    else:
                        print('else_GV')
                        break
                #m
                print('lists : ',lists)
                if len(lists)==1:
                    print('size lists: ',len(lists))
                    comservo.write(b'm')

                    os.remove(path_original)
                    time.sleep(7)
                    Crop(x,y,h,w,path_original,path_crop)
                    print('crop')
                    Resize(path_crop,path_RZ)
                    print('resize')
                    Black_White(path_RZ,path_BW)
                    print('bw')
                    while (1):
                        print('while')
                        tempgetV =getValue_pixel(path_BW)
                        if tempgetV ==1:
                            time.sleep(5)
                            print('===new pic path 1===')
                            path_original = r'C:/out/Pic.bmp'
                            Crop(x,y,h,w,path_original,path_crop)
                            Resize(path_crop,path_RZ)
                            Black_White(path_RZ,path_BW)
                            #getValue_pixel(path_BW)
                            print('---------------')
                        elif tempgetV=="Lower":
                            print('lower_GV')
                            lists.append('O')
                            break
                        elif tempgetV=="Upper":
                            print('upper_GV')
                            lists.append('U')
                            break
                        elif tempgetV=="Left":
                            print('left_GV')
                            lists.append('L')
                            break
                        elif tempgetV=="Right":
                            print('right_GV')
                            lists.append('R')
                            break
                        elif tempgetV=="Top":
                            print('top_GV')
                            lists.append('T')
                            break
                        elif tempgetV=="Buttom":
                            print('bottom_GV')
                            lists.append('B')
                            break
                        else:
                            print('else_GV')
                            break

                    #L   
                    print('lists : ',lists)
                    if len(lists)==2:
                        print('size lists: ',len(lists))
                        comservo.write(b'l')

                        os.remove(path_original)
                        time.sleep(7)
                        Crop(x,y,h,w,path_original,path_crop)
                        print('crop')
                        Resize(path_crop,path_RZ)
                        print('resize')
                        Black_White(path_RZ,path_BW)
                        print('bw')
                        while (1):
                            print('while')
                            tempgetV =getValue_pixel(path_BW)
                            if tempgetV ==1:
                                time.sleep(5)
                                print('===new pic path 1===')
                                path_original = r'C:/out/Pic.bmp'
                                Crop(x,y,h,w,path_original,path_crop)
                                Resize(path_crop,path_RZ)
                                Black_White(path_RZ,path_BW)
                                #getValue_pixel(path_BW)
                                print('---------------')
                            elif tempgetV=="Lower":
                                print('lower_GV')
                                lists.append('O')
                                break
                            elif tempgetV=="Upper":
                                print('upper_GV')
                                lists.append('U')
                                break
                            elif tempgetV=="Left":
                                print('left_GV')
                                lists.append('L')
                                break
                            elif tempgetV=="Right":
                                print('right_GV')
                                lists.append('R')
                                break
                            elif tempgetV=="Top":
                                print('top_GV')
                                lists.append('T')
                                break
                            elif tempgetV=="Buttom":
                                print('bottom_GV')
                                lists.append('B')
                                break
                            else:
                                print('else_GV')
                                break
                        print('lists : ',lists)

    Pule()
    comservo.close()
#-------------------------------------------------------------
#main 

# python control arduino
arduino_servo = serial.Serial('COM10',115200)  
#cam = serial.Serial('COM1',115200)  

TakeBegin(arduino_servo)
"""
path_original = r'C:/out/Pic.bmp'
path_crop=r'C:/image/crop/test.png'
path_BW=r'C:/image/b-w/bw.png'
path_RZ= r'C:/image/crop/resize/h.png'
Crop(x,y,h,w,path_original,path_crop)
Resize(path_crop,path_RZ)
Black_White(path_RZ,path_BW)"""
cv2.waitKey(0)
cv2.destroyAllWindows()