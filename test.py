import cv2 as cv
import match
import bounds
import numpy as np

fn = 0
capture = cv.VideoCapture('clip.mp4')
bBox = bounds.BoundingBox((0,0), 960, 540)
bBox_target = bounds.BoundingBox((0,0), 960, 540)
bBox_prev = None

crop_top = 0
crop_bottom = 50

while capture.isOpened():
    fn +=1
    out, frame = capture.read()
    if(not out):
        break
    points = match.getMatches(frame, crop_top, crop_bottom)
    points = np.column_stack(points)
    frame = cv.resize(frame, (960, 540), interpolation=cv.INTER_NEAREST)
    
    if(len(points) > 0):
        for (y, x) in points:
            cv.circle(frame, (x,y+40), 5, (0,0,255), 2)

        bBox_target = bounds.getBoundingBox(points)
    
    bBox = bounds.interpolateBoxes(bBox, bBox_target)

    bBoxRounded = bounds.roundCoords(bBox)

    cv.circle(frame, (bBoxRounded.pos[0], bBoxRounded.pos[1]+crop_top) , 5, (0,255,255), 2)

    recStart = (bBoxRounded.pos[0], bBoxRounded.pos[1]+crop_top)
    recEnd = (bBoxRounded.pos[0]+bBoxRounded.width, bBoxRounded.pos[1]+bBoxRounded.height+crop_top)

    cv.rectangle(frame, recStart, recEnd, (0,255,255), 1)

    cv.imshow('cringe tracker', cv.resize(frame[recStart[1]:recEnd[1],recStart[0]:recEnd[0]], (960,540)))

    cv.waitKey(1)