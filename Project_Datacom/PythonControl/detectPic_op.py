import cv2 
import serial
import time
import os


#Edit picture
def Crop(path,pathsave):        # function ครอปตรงกลางรูป เริ่มที่ ตำแหน่ง x= 60 y=80 ขนาด 160*160 พิกเซล
    x=60
    y=80
    h=160
    w=160
    img = cv2.imread(path, 0)   # read path รูปที่จะครอป 
    crop = img[y:y+h, x:x+w]    # ทำการ ครอป
    cv2.imwrite(pathsave, crop) # save path ไปที่ ตำแหน่งที่ต้องการ save

def Black_White(path,pathsave): # Function ทำให้รูปสีเข้มขึ้น
    img_grey = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # ทำให้รูปเป็นขาวดำ
    thresh = 64 
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1] # ทำให้รูปสีเข้มขึ้น โดยช่วงค่าสีตั้งแต่ 0-63 เป็นสีขาว และช่วง 64-255 เป็นสีดำ
    cv2.imwrite(pathsave, img_binary) # save path ไปที่ ตำแหน่งที่ต้องการ save

def Resize(path,pathsave): # Function ลดขนาดรูป
    img_Trans = cv2.imread(path,0) # read path รูปที่จะลดขนาด
    W = 4  # เพื่อที่จะย่อภาพให้เหลือ 4*4 พิกเซล
    shape=img_Trans.shape #อ่านค่าขนาดรูป
    height, width = shape #เก็บค่าขนาดรูป  
    imgScale = W/width    
    newX,newY = img_Trans.shape[1]*imgScale, img_Trans.shape[0]*imgScale  # newX,newY เก็บค่า x y 
    newimg = cv2.resize(img_Trans,(int(newX),int(newY)))  # ทำการลดขนาดภาพ
    cv2.imwrite(pathsave, newimg)  # save path ไปที่ ตำแหน่งที่ต้องการ save

def Repicture(path_original,path_crop,path_BW,path_RZ): # function รวมการปรับแต่งรูป
    Crop(path_original,path_crop)   # function ครอปตรงกลางรูป 
    Resize(path_crop,path_RZ)       # Function ลดขนาดรูป
    Black_White(path_RZ,path_BW)    # Function ทำให้รูปสีเข้มขึ้น

def sendXY(comservo,a): # function ส่งค่าตำแหน่งพิกัดของพิกเซล
    d=[]
    i=0
    for y in range(80,201,40): # เริ่มตำแหน่งพิกเซลในภาพที่เลือก detect แนว y ตั้งแต่ พิกัดที่ 80-200 โดยแต่ละแถวห่างกัน 40 พิกเซล
        for x in range (60,181,40): # เริ่มตำแหน่งพิกเซลในภาพที่เลือก detect แนว x ตั้งแต่ พิกัดที่ 60-180 โดยแต่ละคอลัมน์ห่างกัน 40 พิกเซล
            d.append(x)  # ทำการเก็บค่าพิกัด x ให้ PC1   
            d.append(y)  # ทำการเก็บค่าพิกัด y ให้ PC1 
            d.append(a[i])  # ทำการเก็บค่าจุดภาพ ให้ PC1
            i+=1
        print("\t")   
    comservo.write(d)
    return d

#Get value from picture
def getValueNew(path): #function รับจุดภาพจากรูปที่เลือก เป็น 0 1
    lists=[]
    imVN = cv2.imread(path, 0)  # อ่าน path รูปที่เลือก
    rows,cols = imVN.shape      # อ่าน ค่าขนาดรูป
    for y in range(rows):
        for x in range(cols):
            if imVN[y,x]>=128 and imVN[y,x]<=255:  # ถ้าจุดภาพ อยู่ในช่วง 128 - 255 ให้ จุดภาพนั้นมีค่าเป็น 1 (สีดำ)
                imVN[y,x]=1
            else:
                imVN[y,x]=0    # ถ้าจุดภาพ อยู่นอกเหนือ จากช่วง 128 - 255 ให้ จุดภาพนั้นมีค่าเป็น 0 (สีขาว)  
            print(imVN[y,x], end = '')   # แสดงค่าจุดภาพ ขนาด  4*4 
            lists.append(imVN[y,x])
        print("\t")  
    return lists
        
def getValueGrayscal(path):  #function รับจุดภาพจากรูปที่เลือก เป็น ค่า Grayscale
    listsG=[]
    imVG = cv2.imread(path, 0)  # อ่าน path รูปที่เลือก
    rows,cols = imVG.shape      # อ่าน ค่าขนาดรูป
    for y in range(rows):
        for x in range(cols):
            print(imVG[y,x],end=' ') # แสดงจุดภาพ ในช่วง 0 -255 (โดยใช้ภาพที่ทำเป็น Grayscale มาแล้ว )
            listsG.append(imVG[y,x])
        print("\t")
    return listsG

def getValue_pixel(path):#function แสดงจุดภาพและบอกชนิดของภาพ
    imV = cv2.imread(path, 0) 
    rows,cols = imV.shape
    for y in range(rows):
        for x in range(cols):
            if imV[y,x]>=128 and imV[y,x]<=255:
                imV[y,x]=1
            else:
                imV[y,x]=0
    # เช็คจุดภาพว่าเข้ากรณี lower หรือไม่
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
    # เช็คจุดภาพว่าเข้ากรณี upper หรือไม่ 
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
    #เช็คจุดภาพว่าเข้ากรณี left หรือไม่ 
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
    #เช็คจุดภาพว่าเข้ากรณี right หรือไม่ 
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
    #เช็คจุดภาพว่าเข้ากรณี top หรือไม่ 
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
    #เช็คจุดภาพว่าเข้ากรณี bottom หรือไม่ 
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
        return "Bottom"
    else:
        print('\tRead Error ')
        return 1


#control Arduino and take photo
def ReadPicture(lists_pic,comservo): # function ส่งชนิดของรูปที่อ่านได้ให้ PC1
    print('* status picture')
    path_original = r'C:/out/Pic.bmp'
    path_crop     = r'C:/image/crop/crop.png'
    path_BW       = r'C:/image/b-w/bw.png'
    path_RZ       = r'C:/image/crop/resize/resize.png'
    while(True):
        tempgetV =getValue_pixel(path_BW)
        if tempgetV ==1:  # กรณีอ่านรูปไม่ได้
            time.sleep(5)
            print('\tRead new picture')
            Repicture(path_original,path_crop,path_BW,path_RZ)  # อ่านรูปใหม่
        elif tempgetV=="Lower":
            lists_pic.append("5")   # เก็บค่าชนิดของรูปเพื่อให้ PC1 เลือก
            comservo.write(b'5')    # ถ้ารูปเป็น Lower ส่ง 5 ให้ PC1
            break
        elif tempgetV=="Upper":
            lists_pic.append("4")   # เก็บค่าชนิดของรูปเพื่อให้ PC1 เลือก
            comservo.write(b'4')    # ถ้ารูปเป็น Upper ส่ง 4 ให้ PC1
            break
        elif tempgetV=="Left":
            lists_pic.append("2")   # เก็บค่าชนิดของรูปเพื่อให้ PC1 เลือก
            comservo.write(b'2')    # ถ้ารูปเป็น Left ส่ง 2 ให้ PC1
            break
        elif tempgetV=="Right":
            lists_pic.append("3")   # เก็บค่าชนิดของรูปเพื่อให้ PC1 เลือก
            comservo.write(b'3')    # ถ้ารูปเป็น Right ส่ง 3 ให้ PC1
            break
        elif tempgetV=="Top":
            lists_pic.append("0")   # เก็บค่าชนิดของรูปเพื่อให้ PC1 เลือก
            comservo.write(b'0')    # ถ้ารูปเป็น Top ส่ง 0 ให้ PC1
            break
        elif tempgetV=="Bottom":
            lists_pic.append("1")  # เก็บค่าชนิดของรูปเพื่อให้ PC1 เลือก
            comservo.write(b'1')   # ถ้ารูปเป็น Lower ส่ง 1 ให้ PC1
            break
        else:
            break
    return lists_pic         

def TakeBegin(comservo): #function เริ่มการทำงาน 
    lists_pic=[]  # เก็บชนิดภาพที่ถ่ายทั้ง 3 ภาพ  
    # path สำหรับแปลงรูป
    path_original = r'C:/out/Pic.bmp'
    path_crop     = r'C:/image/crop/crop.png'
    path_BW       = r'C:/image/b-w/bw.png'
    path_RZ       = r'C:/image/crop/resize/resize.png'
    # path สำหรับเซฟภาพที่ถ่ายได้ และแปลงเป็นขาวดำแล้ว ทั้ง 3 มุม
    path_BW_NEW1      = r'C:/image/b-w/bw_New1.png'
    path_BW_NEW2      = r'C:/image/b-w/bw_New2.png'
    path_BW_NEW3      = r'C:/image/b-w/bw_New3.png'
    # path สำหรับเซฟภาพที่ถ่ายได้ แต่ไม่ได้ทำเป็นขาวดำ ทั้ง 3 มุม เพื่อหาค่า Grayscale 
    path_RE_NEW1      = r'C:/image/crop/resize/resize1.png'
    path_RE_NEW2      = r'C:/image/crop/resize/resize2.png'
    path_RE_NEW3      = r'C:/image/crop/resize/resize3.png'

    while(True): 
        if(comservo.inWaiting()): # รอรับค่าที่ส่งมาจาก PC1 ซึ่งสั่งให้ PC2 ทำงาน เพื่อเริ่มการหมุนและถ่ายภาพ
            raw = comservo.read()   # เก็บค่าที่อ่านมาจาก Serial ของ PC2
            data = raw.decode('ascii')  # decode ค่า ascii ที่อ่านมาจาก Serial ของ PC2 ให้เป็น char
            print('---------------------')
            print('Com name       :',comservo.name) 
            print('Status arduino :',data)
            print('---------------------')
            #arduino send...
            if data=='S':
                print('===START PROGRAM===')
                raw = comservo.read()   # เก็บค่าที่อ่านมาจาก Serial ของ PC2
                data = raw.decode('ascii')  # decode ค่า ascii ที่อ่านมาจาก Serial ของ PC2 ให้เป็น char
                print('---------------------')
                print('Status  :',data)
                print('---------------------')
                
                if data == 'D': #เมื่อได้รับ D จาก PC2 จะเริ่มหมุนกล้อง
                    print('\nServo move Right >')
                    comservo.write(b'r')    # ส่งคำสั่งให้ PC2 หมุน servo ไปที่มุม 45 องศา
                    raw = comservo.read()   # เก็บค่าที่อ่านมาจาก Serial ของ PC2 ซึ่งจะบอกว่า servo หันไปแล้ว
                    data = raw.decode('ascii')  # decode ค่า ascii ที่อ่านมาจาก Serial ของ PC2 ให้เป็น char
                    print('status servo : ',data)

                    # take photo 0
                    print('\n==start camera ==')
                    print('statas  : 0 radius')
                    os.remove(path_original)    # ลบรูปที่เคยถ่ายไว้ เพื่อรีเซ็ตรูป
                    time.sleep(10)              # เว้นช่วงเวลา 10 วินาทีหลังจากลบรูป เพื่อรอรับรูปใหม่
                    Repicture(path_original,path_crop,path_BW,path_RZ)  # เรียกใช้ Function รวมการปรับแต่งรูปที่เริ่มถ่ายใหม่
                    
                    print('* Repicture finish')
                    ReadPicture(lists_pic,comservo) # เรียกใช้ Function บอกชนิดของรูปและส่งชิดของรูปให้ PC1
                    print('Read finish > Temp Picture : ',lists_pic)
                    Resize(path_crop,path_RE_NEW1)  # เรียกใช้ Function ลดขนาดรูป เพื่อนำรูปที่สามารถระบุชนิดได้ถูกต้องไปลดขนาด เพื่อนำไปใช้ในการบอกค่า Grayscale ต่อไป
                    Black_White(path_BW,path_BW_NEW1) # เรียกใช้ Function ปรับสีรูปให้เข้มขึ้น เพื่อนำรูปที่สามารถระบุชนิดได้ถูกต้องไปปรับสีรูปให้เข้มขึ้น เพื่อนำไปใช้ในการบอกค่า Binary 0 1 ต่อไป
                    print('--------------------------------------------')
                    if len(lists_pic)==1: # เช็คจำนวนรูป หาก lists_pic = 1 แสดงว่าในมุม 45 องศามีรูปที่ถ่ายเสร็จแล้วและสามารถระบุชนิดของรูปได้ถูกต้อง
                        print('--------------------------------------------')
                        print('\nServo move Miduim >')
                        comservo.write(b'm') # ส่งคำสั่งให้ PC2 หมุน servo ไปที่มุม 0 องศา
                        raw = comservo.read() # เก็บค่าที่อ่านมาจาก Serial ของ PC2 ซึ่งจะบอกว่า servo หันไปแล้ว
                        data = raw.decode('ascii') # decode ค่า ascii ที่อ่านมาจาก Serial ของ PC2 ให้เป็น char
                        print('status servo : ',data)

                        # take photo 45
                        print('\n==start camera ==')
                        print('statas  : 45 radius')
                        os.remove(path_original) # ลบรูปที่เคยถ่ายไว้ เพื่อรีเซ็ตรูป
                        time.sleep(10)           # เว้นช่วงเวลา 10 วินาทีหลังจากลบรูป เพื่อรอรับรูปใหม่
                        Repicture(path_original,path_crop,path_BW,path_RZ) # เรียกใช้ Function รวมการปรับแต่งรูปที่เริ่มถ่ายใหม่
                        print('* Repicture finish')
                        ReadPicture(lists_pic,comservo) # เรียกใช้ Function บอกชนิดของรูปและส่งชิดของรูปให้ PC1
                        print('Read finish > Temp Picture : ',lists_pic)
                        Resize(path_crop,path_RE_NEW2) # เรียกใช้ Function ลดขนาดรูป เพื่อนำรูปที่สามารถระบุชนิดได้ถูกต้องไปลดขนาด เพื่อนำไปใช้ในการบอกค่า Grayscale ต่อไป
                        Black_White(path_BW,path_BW_NEW2) # เรียกใช้ Function ปรับสีรูปให้เข้มขึ้น เพื่อนำรูปที่สามารถระบุชนิดได้ถูกต้องไปปรับสีรูปให้เข้มขึ้น เพื่อนำไปใช้ในการบอกค่า Binary 0 1 ต่อไป
                        print('--------------------------------------------')
                        if len(lists_pic)==2: # เช็คจำนวนรูป หาก lists_pic = 2 แสดงว่าในมุม 0 องศามีรูปที่ถ่ายเสร็จแล้วและสามารถระบุชนิดของรูปได้ถูกต้อง
                            print('--------------------------------------------')
                            print('\nServo move Left >')
                            comservo.write(b'l') # ส่งคำสั่งให้ PC2 หมุน servo ไปที่มุม -45 องศา
                            raw = comservo.read() # เก็บค่าที่อ่านมาจาก Serial ของ PC2 ซึ่งจะบอกว่า servo หันไปแล้ว
                            data = raw.decode('ascii') # decode ค่า ascii ที่อ่านมาจาก Serial ของ PC2 ให้เป็น char
                            print('status servo : ',data)

                            # take photo 90
                            print('\n==start camera ==')
                            print('statas  : 90 radius')
                            os.remove(path_original) # ลบรูปที่เคยถ่ายไว้ เพื่อรีเซ็ตรูป
                            time.sleep(10) # เว้นช่วงเวลา 10 วินาทีหลังจากลบรูป เพื่อรอรับรูปใหม่
                            Repicture(path_original,path_crop,path_BW,path_RZ) # เรียกใช้ Function รวมการปรับแต่งรูปที่เริ่มถ่ายใหม่
                            print('* Repicture finish')
                            ReadPicture(lists_pic,comservo) # เรียกใช้ Function บอกชนิดของรูปและส่งชิดของรูปให้ PC1
                            print('Read finish > Temp Picture : ',lists_pic)
                            Resize(path_crop,path_RE_NEW3) # เรียกใช้ Function ลดขนาดรูป เพื่อนำรูปที่สามารถระบุชนิดได้ถูกต้องไปลดขนาด เพื่อนำไปใช้ในการบอกค่า Grayscale ต่อไป
                            Black_White(path_BW,path_BW_NEW3) # เรียกใช้ Function ปรับสีรูปให้เข้มขึ้น เพื่อนำรูปที่สามารถระบุชนิดได้ถูกต้องไปปรับสีรูปให้เข้มขึ้น เพื่อนำไปใช้ในการบอกค่า Binary 0 1 ต่อไป
                            print('--------------------------------------------')
                            if len(lists_pic)==3: # เช็คจำนวนรูป หาก lists_pic = 3 แสดงว่าในมุม -45 องศามีรูปที่ถ่ายเสร็จแล้วและสามารถระบุชนิดของรูปได้ถูกต้อง
                                print('\nComplete ! >')
                                comservo.write(b'C')  #ส่งคำสั่งให้ PC2 ทราบว่าถ่ายได้ครบ 3 รูปแล้ว และรอรับคำสั่งต่อไป
                                print('--------------------------------------------')
            
                raw1 = comservo.read() # เก็บค่าที่อ่านมาจาก Serial ของ PC2 ซึ่งจะบอกว่า PC1 เลือกรูปอะไรมา
                data = raw1.decode('ascii') # decode ค่า ascii ที่อ่านมาจาก Serial ของ PC2 ให้เป็น char
                print('choose : ',data) 

                if data == 'T': # หาก data เป็น T แสดงว่า PC1 เลือกรูป Top
                    print('== TOP status ==')    
                    # นำรูปทั้ง 3 รูปที่เก็บไว้มาเช็คว่ารูปใดคือ Top
                    ch1=getValue_pixel(path_BW_NEW1) 
                    ch2=getValue_pixel(path_BW_NEW2)
                    ch3=getValue_pixel(path_BW_NEW3)
                    if ch1=='Top': # ถ้ารูปที่ 1 เป็น Top
                        print('\t*PATH 1')
                        a=getValueNew(path_BW_NEW1) # นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW1) # นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 1')
                        print('Rtop1 :',a)
                        print('Gtop1 :',b)
                        print('XY   :',c)
                    elif ch2=='Top': # ถ้ารูปที่ 2 เป็น Top
                        print('\t*PATH 2')
                        a=getValueNew(path_BW_NEW2)  #นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW2) # นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 2')
                        print('Rtop2 :',a)
                        print('Gtop2 :',b)
                        print('XY   :',c)
                    elif ch3=='Top': # ถ้ารูปที่ 3 เป็น Top
                        print('\t*PATH 3')
                        a=getValueNew(path_BW_NEW3) #นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW3) # นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 3')
                        print('Rtop3 :',a)
                        print('Gtop3 :',b)
                        print('XY   :',c)

                elif data == 'B': # หาก data เป็น B แสดงว่า PC1 เลือกรูป Buttom
                    print('== BOTTOM status ==')
                    # นำรูปทั้ง 3 รูปที่เก็บไว้มาเช็คว่ารูปใดคือ Buttom
                    ch1=getValue_pixel(path_BW_NEW1) 
                    ch2=getValue_pixel(path_BW_NEW2)
                    ch3=getValue_pixel(path_BW_NEW3)
                    if ch1=='Bottom':
                        print('\t*PATH 1')
                        a=getValueNew(path_BW_NEW1) #นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW1) # นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 1')
                        print('Rbot1 :',a)
                        print('Gbot1 :',b)
                        print('XY   :',c)
                    elif ch2=='Bottom':
                        print('\t*PATH 2')
                        a=getValueNew(path_BW_NEW2) #นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW2) # นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 2')
                        print('Rbot2 :',a)
                        print('Gbot2 :',b)
                        print('XY   :',c)
                    elif ch3=='Bottom':
                        print('\t*PATH 3')
                        a=getValueNew(path_BW_NEW3) #นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW3) # นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 3')
                        print('Rbot3 :',a)
                        print('Gbot3 :',b)
                        print('XY   :',c)

                elif data == 'L': # หาก data เป็น L แสดงว่า PC1 เลือกรูป Left
                    print('== LEFT status ==')
                    # นำรูปทั้ง 3 รูปที่เก็บไว้มาเช็คว่ารูปใดคือ Left
                    ch1=getValue_pixel(path_BW_NEW1) 
                    ch2=getValue_pixel(path_BW_NEW2)
                    ch3=getValue_pixel(path_BW_NEW3)
                    if ch1=='Left':
                        print('\t*PATH 1')
                        a=getValueNew(path_BW_NEW1) #นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW1) # นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 1')
                        print('Rlef1 :',a)
                        print('Glef1 :',b)
                        print('XY    :',c)
                    elif ch2=='Left':
                        print('\t*PATH 2')
                        a=getValueNew(path_BW_NEW2) #นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW2) # นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 2')
                        print('Rlef2 :',a)
                        print('Glef2 :',b)
                        print('XY    :',c)
                    elif ch3=='Left':
                        print('\t*PATH 3')
                        a=getValueNew(path_BW_NEW3) #นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW3) # นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 3')
                        print('Rlef3 :',a)
                        print('Glef3 :',b)
                        print('XY    :',c)

                elif data == 'R': # หาก data เป็น R แสดงว่า PC1 เลือกรูป Right
                    print('== RIGHT status ==')
                    # นำรูปทั้ง 3 รูปที่เก็บไว้มาเช็คว่ารูปใดคือ Right
                    ch1=getValue_pixel(path_BW_NEW1) 
                    ch2=getValue_pixel(path_BW_NEW2)
                    ch3=getValue_pixel(path_BW_NEW3)
                    if ch1=='Right':
                        print('\t*PATH 1')
                        a=getValueNew(path_BW_NEW1) #นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW1) # นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 1')
                        print('Rrig1 :',a)
                        print('Grig1 :',b)
                        print('XY    :',c)
                    elif ch2=='Right':
                        print('\t*PATH 2')
                        a=getValueNew(path_BW_NEW2) #นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW2) # นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 2')
                        print('Rrig2 :',a)
                        print('Grig2 :',b)
                        print('XY    :',c)
                    elif ch3=='Right':
                        print('\t*PATH 3')
                        a=getValueNew(path_BW_NEW3) #นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW3) # นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale ให้ PC1
                        print('\t*SEND PATH 3')
                        print('Rrig3 :',a)
                        print('Grig3 :',b)
                        print('XY    :',c)

                elif data == 'U': # หาก data เป็น U แสดงว่า PC1 เลือกรูป Upper
                    print('== UPPER status ==')
                    # นำรูปทั้ง 3 รูปที่เก็บไว้มาเช็คว่ารูปใดคือ Upper
                    ch1=getValue_pixel(path_BW_NEW1) 
                    ch2=getValue_pixel(path_BW_NEW2)
                    ch3=getValue_pixel(path_BW_NEW3)
                    if ch1=='Upper':
                        print('\t*PATH 1')
                        a=getValueNew(path_BW_NEW1) #นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW1) # นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale  ให้ PC1
                        print('\t*SEND PATH 1')
                        print('Rupp1 :',a)
                        print('Gupp1 :',b)
                        print('XY    :',c)
                    elif ch2=='Upper':
                        print('\t*PATH 2')
                        a=getValueNew(path_BW_NEW2) #นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW2) # นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale  ให้ PC1
                        print('\t*SEND PATH 2')
                        print('Rupp2 :',a)
                        print('Gupp2 :',b)
                        print('XY    :',c)
                    elif ch3=='Upper':
                        print('\t*PATH 3')
                        a=getValueNew(path_BW_NEW3) #นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW3) # นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale  ให้ PC1
                        print('\t*SEND PATH 3')
                        print('Rupp3 :',a)
                        print('Gupp3 :',b)
                        print('XY    :',c)

                elif data == 'O': # หาก data เป็น O แสดงว่า PC1 เลือกรูป Lower
                    print('== LOWER status ==')
                    # นำรูปทั้ง 3 รูปที่เก็บไว้มาเช็คว่ารูปใดคือ Upper
                    ch1=getValue_pixel(path_BW_NEW1) 
                    ch2=getValue_pixel(path_BW_NEW2)
                    ch3=getValue_pixel(path_BW_NEW3)
                    if ch1=='Lower':
                        print('\t*PATH 1')
                        a=getValueNew(path_BW_NEW1) #นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW1) # นำรูป 1 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale  ให้ PC1
                        print('\t*SEND PATH 1')
                        print('Rlow1 :',a)
                        print('Glow1 :',b)
                        print('XY    :',c)
                    elif ch2=='Lower':
                        print('\t*PATH 2')
                        a=getValueNew(path_BW_NEW2) #นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW2) # นำรูป 2 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale  ให้ PC1
                        print('\t*SEND PATH 2')
                        print('Rlow2 :',a)
                        print('Glow2 :',b)
                        print('XY    :',c)
                    elif ch3=='Lower':
                        print('\t*PATH 3')
                        a=getValueNew(path_BW_NEW3) #นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Binary 0 1 อีกครั้ง เพื่อเตรียมส่งให้ PC1
                        b=getValueGrayscal(path_RE_NEW3) # นำรูป 3 ที่เก็บไว้มาหาค่าจุดภาพเป็น Grayscale เพื่อเตรียมส่งให้ PC1
                        c=sendXY(comservo,b) # ส่งค่าพิกัดพิกเซล (x,y) และจุดภาพเป็น Grayscale  ให้ PC1
                        print('\t*SEND PATH 3')
                        print('Rlow3 :',a)
                        print('Glow3 :',b)
                        print('XY    :',c)
            
            if data=='E':
                print('=== END PROGRAM ===') 
                break

            
        #break    
    #return lists_pic
    
#----------------------------------------------------------------
#main 
arduino_servo = serial.Serial('COM17',115200)  # ตั้งค่าให้ python เชื่อมต่อกับ arduino COM17 ผ่าน Serial ที่ 115200 baud
TakeBegin(arduino_servo)
#print('TakeBegin : ',r)
arduino_servo.close()

