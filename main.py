from unittest import result
import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) #Escolhendo a webcam, poderia ser 0,1,2... dependendo d0 numero de webcams 

mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

pTime = 0 # Previous time
cTime = 0 # Current time

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:

        for handLandmarks in results.multi_hand_landmarks:

            for id, landmark in enumerate(handLandmarks.landmark):
                # print(id, landmark)
                height, width, channels = img.shape # Pegando o tamanho do video
                cx, cy = int(landmark.x * width), int(landmark.y * height) # Pegandos as coordenadas de cada ponto em px
                print(id, f"X: {cx}", f"Y: {cy}")

                # if id == 0:
                        # Desenhando um circulo no ponto com o respectivo id
                        # Atributos (imagem, posição, raio dom circulo, cor, circulo como cheio(opcional))
                    # cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        
            mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

    
    cTime = time.time()
    fps = 1/(cTime - pTime) # calculando o fps do video
    pTime = cTime

    # Colocando o fps na tela
    # Atributos (imagem, texto, posição, font, tamanho, cor, grossura)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) 

    cv2.imshow("Image", img)
    cv2.waitKey(1)
