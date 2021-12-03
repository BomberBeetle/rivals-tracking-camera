import cv2 as cv
import match
import bounds
import numpy as np

fn = 0
capture = cv.VideoCapture('clip.mp4')
bBox_prev = None
while capture.isOpened():
    fn +=1
    _, frame = capture.read()

    points = match.getMatches(frame)
    points = np.column_stack(points)
    frame = cv.resize(frame, (960, 540), interpolation=cv.INTER_NEAREST)

    if(len(points) > 0):
        for (y, x) in points:
            cv.circle(frame, (x,y+40), 5, (0,0,255), 2)

        bBox = bounds.getBoundingBox(points)

        if(bBox.width > 960):
            bBox.width = 960
        if(bBox.height > 540):
            bBox.height = 540

        if(bBox.pos[0] < 0):
            bBox.pos = (0, bBox.pos[1])
        elif(bBox.pos[0]+bBox.width > 960):
            bBox.pos =  (960 - bBox.width, bBox.pos[1])

        if(bBox.pos[1] < 0):
            bBox.pos = (bBox.pos[0],0)
        elif(bBox.pos[1] + bBox.height > 540):
            bBox.pos =  (bBox.pos[0],540-bBox.height)

        if(bBox_prev != None):
            bBox = bounds.interpolateBoxes(bBox_prev, bBox)

        bBox_prev = bBox

        bBoxRounded = bounds.roundCoords(bBox)

        cv.circle(frame, (bBoxRounded.pos[0], bBoxRounded.pos[1]+40) , 5, (0,255,255), 2)

        recStart = (bBoxRounded.pos[0], bBoxRounded.pos[1]+40)
        recEnd = (bBoxRounded.pos[0]+bBoxRounded.width, bBoxRounded.pos[1]+bBoxRounded.height+40)

        cv.rectangle(frame, recStart, recEnd, (0,255,255), 1)

        cv.imshow('cringe tracker', cv.resize(frame[recStart[1]:recEnd[1],recStart[0]:recEnd[0]], (1280, 720)))

    cv.waitKey(1)