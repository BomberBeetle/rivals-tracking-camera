import cv2 as cv
import match
import bounds
import numpy as np

fn = 0
capture = cv.VideoCapture('r2r.mp4')
bBox = bounds.BoundingBox((0,0), 960, 540)
bBox_target = bounds.BoundingBox((0,0), 960, 540)
bBox_prev = None

crop_top = 20
crop_bottom = 50

while capture.isOpened():
    fn +=1
    _, frame = capture.read()

    points = match.getMatches(frame, crop_top, crop_bottom)
    points = np.column_stack(points)
    frame = cv.resize(frame, (960, 540), interpolation=cv.INTER_NEAREST)
    
    if(len(points) > 0):
        for (y, x) in points:
            cv.circle(frame, (x,y+40), 5, (0,0,255), 2)

        bBox_target = bounds.getBoundingBox(points)

        if(bBox_target.width > 960):
            bBox_target.width = 960
        if(bBox_target.height > 540):
            bBox_target.height = 540

        if(bBox_target.pos[0] < 0):
            bBox_target.pos = (0, bBox_target.pos[1])
        elif(bBox_target.pos[0]+bBox_target.width > 960):
            bBox_target.pos =  (960 - bBox_target.width, bBox_target.pos[1])

        if(bBox_target.pos[1] < 0):
            bBox_target.pos = (bBox_target.pos[0],0)
        elif(bBox_target.pos[1] + bBox_target.height > 540):
            bBox_target.pos =  (bBox_target.pos[0],540-bBox_target.height)

    
    bBox = bounds.interpolateBoxes(bBox, bBox_target)

    bBoxRounded = bounds.roundCoords(bBox)

    cv.circle(frame, (bBoxRounded.pos[0], bBoxRounded.pos[1]+crop_top) , 5, (0,255,255), 2)

    recStart = (bBoxRounded.pos[0], bBoxRounded.pos[1]+crop_top)
    recEnd = (bBoxRounded.pos[0]+bBoxRounded.width, bBoxRounded.pos[1]+bBoxRounded.height+crop_top)

    cv.rectangle(frame, recStart, recEnd, (0,255,255), 1)

    cv.imshow('cringe tracker', cv.resize(frame[recStart[1]:recEnd[1],recStart[0]:recEnd[0]], (960,540)))

    cv.waitKey(1)