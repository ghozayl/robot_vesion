


import math
import cv2 
import numpy as np
import mediapipe as mp
from robodk.robolink import * 

RDK = Robolink()
import time

frameWidth = 640
frameHeight = 480

cpx=int(frameWidth/2)
cpy=int(frameHeight/2)

maxlen=120
minlen=30

open=85
close=0

robot=RDK.Item('',ITEM_TYPE_ROBOT)


target = RDK.Item('Target 1')
target2 = RDK.Item('Target 2')
target3 = RDK.Item('Target 3')
target4 = RDK.Item('Target 4')
target5 = RDK.Item('Target 5')
target_pose = target.Pose()
xyz_ref = target_pose.Pos()



tips = [4,8,12,16,20]
cap=cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)

mphands=mp.solutions.hands

hands=mphands.Hands()

mpdraw=mp.solutions.drawing_utils

#draw=mp.solutions.drawing_utils
draw=mp.solutions.drawing_styles
ptime=0
ctime=0

def finger_fun(limx,limy,tips):
    finger_state=[]

    for id in tips :
        if id ==4:
            if limx[17]-limx[4] > 100:
                finger_state.append(1)
            
            else:finger_state.append(0)
        else:
            if limy[id] < limy[id-2] :
             finger_state.append(1)   
            else:finger_state.append(0)

    return finger_state

while True :
    
    _ ,img =cap.read()
    img = cv2.flip(img,1)
    cv2.circle(img,(cpx, cpy),15,(255,0,0),cv2.FILLED)

    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgrgb)
    
    if results.multi_hand_landmarks :
        for handlms in results.multi_hand_landmarks :
            lim_list=[]
            limx=[]
            limy=[]
            for id ,lm in enumerate(handlms.landmark):
                lim_list.append(lm)
                h,w,c= img.shape
                cx=int(w * lm.x)
                cy=int(h * lm.y)
                #print(cx,cy)
                limx.append(cx)
                limy.append(cy)
                
                mpdraw.draw_landmarks(img, handlms,mphands.HAND_CONNECTIONS)

            
            
            
        finger=finger_fun(limx,limy,tips)
        print(finger)

        
        if finger == [0,1,0,0,0]:
            cv2.putText(img,'Target 1',(200,300),cv2.FONT_HERSHEY_COMPLEX,
                   1,(0,0,255),thickness=1)
            robot.MoveJ(target)
            robot.RunInstruction('Program_Done')
        if finger == [0,1,1,0,0]:
            cv2.putText(img,'Target 2',(200,300),cv2.FONT_HERSHEY_COMPLEX,
                   1,(0,0,255),thickness=1)
            robot.MoveJ(target2)
            robot.RunInstruction('Program_Done')
        if finger == [0,1,1,1,0]:
            cv2.putText(img,'Target 3 ',(200,300),cv2.FONT_HERSHEY_COMPLEX,
                   1,(0,0,255),thickness=1)
            robot.MoveJ(target3)
            robot.RunInstruction('Program_Done') 


        if finger == [0,1,1,1,1]:
            cv2.putText(img,'Target 4 ',(200,300),cv2.FONT_HERSHEY_COMPLEX,
                   1,(0,0,255),thickness=1)
            robot.MoveJ(target4)
            robot.RunInstruction('Program_Done') 

        if finger == [1,1,1,1,1]:
            cv2.putText(img,'Target 5 ',(200,300),cv2.FONT_HERSHEY_COMPLEX,
                   1,(0,0,255),thickness=1)
            robot.MoveJ(target5)
            robot.RunInstruction('Program_Done')            

            


            
              
            
            
    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    #print(fps)
    
    cv2.putText(img,str(int(fps)),(50,450),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow('first',img)
    cv2.waitKey(1)

