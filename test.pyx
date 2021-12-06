import cv2 as cv
import match
import bounds
import filter_and_thresh as pfilter
import sys

import numpy as np
cimport numpy as np
np.import_array()

cdef extern from "bounding_boxes.h":
    struct f_BoundingBox:
        float pos[2]
        float width
        float height
        
    struct i_BoundingBox:
        int pos[2]
        int width
        int height

captureStr = 'roubo.mp4'

#bBox = bounds.BoundingBox((0,0), 960, 540)
cdef f_BoundingBox bBox
bBox.pos = [0,0]
bBox.width = 960
bBox.height = 540

cdef f_BoundingBox bBox_target
bBox_target.pos = [0,0]
bBox_target.width = 960
bBox_target.height = 540

cdef i_BoundingBox bBoxRounded

cdef np.ndarray points = np.empty((0,3))

#if(len(sys.argv) > 0):
#    captureStr = sys.argv[0]

capture = cv.VideoCapture(captureStr)

cdef int crop_top = 20
cdef int crop_bottom = 50
cdef int crop_sides = 20

cdef (int, int) recStart 
cdef (int, int) recEnd

cdef np.ndarray new_points
cdef np.ndarray frame
cdef np.ndarray npoints_tresh


while capture.isOpened():
    out, frame = capture.read()
    if(not out):
        break
    new_points = match.getMatches(frame, crop_top, crop_bottom, crop_sides)
    npoints_tresh = np.array([[1.0] for _ in range(new_points.shape[0]) ])
    new_points = np.column_stack((new_points, npoints_tresh))
    points = np.concatenate((points, new_points), axis=0)
    points = pfilter.filter_points_and_apply_threshold(points, 0.1)
    
    frame = cv.resize(frame, (960, 540), interpolation=cv.INTER_NEAREST)
    #frame_d = frame.copy()
    
    if(points.shape[0] > 0):
        #for (y, x, _) in points:
            #y = int(y)
            #x = int(x)
            #cv.circle(frame_d, (x,y+40), 5, (0,0,255), 2)

        bBox_target = bounds.getBoundingBox(points)
        #bBox_target_d = bounds.roundCoords(bBox_target)
        #cv.rectangle(frame_d, (bBox_target_d.pos[0]+crop_sides, bBox_target_d.pos[1]+crop_top), (bBox_target_d.pos[0]+bBox_target_d.width+crop_sides, bBox_target_d.pos[1]+bBox_target_d.height+crop_bottom), (255, 255, 0), 2)
    
    bBox = bounds.interpolateBoxes(bBox, bBox_target)

    bBoxRounded = bounds.roundCoords(bBox)

    #cv.circle(frame_d, (bBoxRounded.pos[0], bBoxRounded.pos[1]+crop_top) , 5, (0,255,255), 2)

    recStart = (bBoxRounded.pos[0]+crop_sides, bBoxRounded.pos[1]+crop_top)
    recEnd = (bBoxRounded.pos[0]+bBoxRounded.width+crop_sides, bBoxRounded.pos[1]+bBoxRounded.height+crop_top)

    #cv.rectangle(frame_d, recStart, recEnd, (0,255,255), 1)

    cv.imshow('cringe tracker', cv.resize(frame[recStart[1]:recEnd[1],recStart[0]:recEnd[0]], (960,540)))
    #cv.imshow('debug', cv.resize(frame_d, (960,540)))
    

    cv.waitKey(1)