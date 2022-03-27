import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



wCam, hCam = 640, 480 # Definindo tamanho do video

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
    
cTime = 0
pTime = 0

detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2] # Posição da ponta do polegar
        x2, y2 = lmList[8][1], lmList[8][2] # Posição da ponta do dedo indicador

        cx, cy =(x1+x2)//2, (y1 + y2)//2 # Centro entre o dedo polegar e o indicador

        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

        lenght = math.hypot(x2 - x1, y2 - y1) # math.hypot() calcula a distancia entre a origem e as coordenadas passadas
        # print(lenght)

        #  Hand Range 20 - 180
        #  Volume range -65 - 0

        vol = np.interp(lenght, [20, 180], [minVol, maxVol])
        percent = (int(vol) * 100) / (minVol * -1) * -1
        print(-(int(vol) * 1.5625))
        # volume.SetMasterVolumeLevel(vol, None)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) 


    cv2.imshow("Img", img)
    cv2.waitKey(1)