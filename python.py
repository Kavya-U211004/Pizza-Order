import os
import cv2 as cv
import cvzone as cz
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector

cap=cv.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

imgBack=cv.imread("Images\Background.png")

folderModes="Images\Modes"
imgPath=os.listdir(folderModes)
imgList=[]
for i in imgPath:
    imgList.append(cv.imread(os.path.join(folderModes,i)))

modeType=0
detector=HandDetector(detectionCon=0.8, maxHands=1)
selection=-1
counter=0

sp=selectionSpeed=5
modePositions=[(1136,196),(1000,384),(1136,581)]
counterPause=0

while True:
    ret,img=cap.read()
    hands,img=detector.findHands(img)
    imgBack[139:139+480,50:50+640]=img
    imgBack[0:720,847:1280]=imgList[modeType]

    if hands and counterPause==0 and modeType<3:
        hand1=hands[0]
        finger1=detector.fingersUp(hand1)
        
        if finger1==[0,1,0,0,0]:
            if selection!=1:
                counter=1
            selection=1
        elif finger1==[0,1,1,0,0,]:
            if selection!=2:
                counter=1
            selection=2
        elif finger1==[0,1,1,1,0]:
            if selection!=3:
                counter=1
            selection=3
        else:
            selection=-1
            counter=0

        if counter>0:
            counter+=1

            cv.ellipse(imgBack,modePositions[selection-1],(103,103),0,0,counter*sp,(0,255,0),20)
            if counter*sp>360:
                modeType+=1
                counter=0
                selection=-1
                counterPause=1

    if counterPause>0:
        counterPause+=1
        if counterPause>60:
            counterPause=0
    
    cv.imshow("Window",imgBack)
    key=cv.waitKey(1)
    if (key==81 or key==113):
        break

cap.release()
cv.destroyAllWindows()


     

