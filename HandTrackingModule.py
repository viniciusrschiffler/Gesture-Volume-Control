from unittest import result
import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self):

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils



    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return img
                    

    def findPosition(self, img):

        landmarkList = []
        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:

                for id, landmark in enumerate(handLandmarks.landmark):

                    height, width, channels = img.shape # Pegando o tamanho do video
                    cx, cy = int(landmark.x * width), int(landmark.y * height) # Pegandos as coordenadas de cada ponto em px

                    landmarkList.append([id, cx, cy])

        return landmarkList            
