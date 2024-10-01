import numpy as np
import pyautogui
from  datetime import datetime
import os
import cv2


filename = "Enregistement"+str(datetime.now())+".avi"
frames_per_second = 24.0
fr=cv2.VideoWriter_fourcc('M','P','4','V')
mydimension= pyautogui.size()
mytype="'M','P','4'"

cap = cv2.VideoCapture(0)
out = cv2.VideoWriter(filename,fr, 25.0, (640,480))
x=0
b=pyautogui.confirm(' Enregistrement avec votre camera active')
if b=="OK":
        
        while True:
            ret, frame = cap.read()
            out.write(frame)
            #cv2.imshow('frame',frame)
            if x==0:
                print('En cours d enregistrement...')
                x=x+1
    
    


cap.release()
out.release()
cv2.destroyAllWindows
if x!=0:
 print('Enregistrement termine la video a ete enregistre dans le fichier:')
 print(filename)
else :
    print(' Enregistrement a echoue')
