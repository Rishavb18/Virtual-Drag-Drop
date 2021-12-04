import cv2 as cv
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=2)
coloR = (255, 0, 255)


cx, cy, w, h = 50, 50, 130, 130


class DragRect():
    def __init__(self, posCenter, size=[130,130]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):

        cx, cy =self.posCenter
        w, h = self.size

        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
            coloR=0,255,0
            self.posCenter = cursor
        else:
            coloR=255,0,255

rectList=[]
for x in range(5):
    rectList.append(DragRect([x*150+50,50]))

while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    hands, img = detector.findHands(img)

    if hands:
        hand1=hands[0]
        lmList1 = hand1["lmList"]

        if lmList1:
            l,_,_ = detector.findDistance(lmList1[8], lmList1[12], img)
            print(l)
            if l<=30:
                cursor = lmList1[8]
                for rect in rectList:
                    rect.update(cursor)

    for rect in rectList:
        cx, cy =rect.posCenter
        w, h = rect.size

        cv.rectangle(img, (cx-w//2,cy-h//2),(cx+w//2,cy+h//2),coloR,cv.FILLED)
        cvzone.cornerRect(img,(cx-w//2,cy-h//2, w, h), 20, rt=0 )

    cv.imshow('Image', img)
    cv.waitKey(1)





