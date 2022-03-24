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

    


def main():
    pTime = 0 # Previous time
    cTime = 0 # Current time

    #Escolhendo a webcam, poderia ser 0,1,2... dependendo d0 numero de webcams 
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        landmarksPositions = detector.findPosition(img)

        cTime = time.time()
        fps = 1/(cTime - pTime) # calculando o fps do video
        pTime = cTime

        # Colocando o fps na tela
        # Atributos (imagem, texto, posição, font, tamanho, cor, grossura)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) 

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
