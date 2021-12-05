import cv2 as cv
import match
import bounds
import numpy as np
import filter_and_thresh as pfilter
import sys

captureStr = 'hitstun.mp4'
fn = 0

bBox = bounds.BoundingBox((0,0), 960, 540)
bBox_target = bounds.BoundingBox((0,0), 960, 540)
points = np.empty((0,3))

#if(len(sys.argv) > 0):
#    captureStr = sys.argv[0]

capture = cv.VideoCapture(captureStr)

crop_top = 20
crop_bottom = 50
crop_sides = 20

while capture.isOpened():
    fn +=1
    out, frame = capture.read()
    if(not out):
        break
    new_points = match.getMatches(frame, crop_top, crop_bottom, crop_sides)
    new_points = np.column_stack(new_points)
    npoints_tresh = np.array([[1.0] for _ in range(new_points.shape[0]) ])
    new_points = np.column_stack((new_points, npoints_tresh))
    points = np.concatenate((points, new_points), axis=0)
    points = pfilter.filter_points_and_apply_threshold(points, 1/10, 0)
    
    frame = cv.resize(frame, (960, 540), interpolation=cv.INTER_NEAREST)
    frame_d = frame.copy()
    
    if(len(points) > 0):
        for (y, x, _) in points:
            y = int(y)
            x = int(x)
            cv.circle(frame_d, (x,y+40), 5, (0,0,255), 2)

        bBox_target = bounds.getBoundingBox(points)
        bBox_target_d = bounds.roundCoords(bBox_target)
        cv.rectangle(frame_d, (bBox_target_d.pos[0]+crop_sides, bBox_target_d.pos[1]+crop_top), (bBox_target_d.pos[0]+bBox_target_d.width+crop_sides, bBox_target_d.pos[1]+bBox_target_d.height+crop_bottom), (255, 255, 0), 2)
    
    bBox = bounds.interpolateBoxes(bBox, bBox_target)

    bBoxRounded = bounds.roundCoords(bBox)

    cv.circle(frame_d, (bBoxRounded.pos[0], bBoxRounded.pos[1]+crop_top) , 5, (0,255,255), 2)

    recStart = (bBoxRounded.pos[0]+crop_sides, bBoxRounded.pos[1]+crop_top)
    recEnd = (bBoxRounded.pos[0]+bBoxRounded.width+crop_sides, bBoxRounded.pos[1]+bBoxRounded.height+crop_top)

    cv.rectangle(frame_d, recStart, recEnd, (0,255,255), 1)
    
    cv.imshow('cringe tracker', cv.resize(frame[recStart[1]:recEnd[1],recStart[0]:recEnd[0]], (960,540)))
    cv.imshow('debug', cv.resize(frame_d, (960,540)))
    

    cv.waitKey(1)