import cv2 as cv
import numpy as np
import os

template = cv.imread(os.path.dirname(__file__) + '/template_percent.png')
#template = cv.resize(template, (template.shape[0]//2, template.shape[1]//2), interpolation=cv.INTER_NEAREST)
template = cv.cvtColor(template, cv.COLOR_BGR2GRAY) 

mask = cv.imread(os.path.dirname(__file__) + '/template_percent_mask.png')
#mask = cv.resize(mask, (mask.shape[0]//2, mask.shape[1]//2), interpolation=cv.INTER_NEAREST)
mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY) 

def getMatches(frame, crop_top=0, crop_bottom=60, crop_sides=0):

    frame = cv.resize(frame, (960, 540), interpolation=cv.INTER_NEAREST)
    frame = frame[crop_top:540-crop_bottom,crop_sides:960-crop_sides]
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    match =cv.matchTemplate(frame_gray, template, cv.TM_CCORR_NORMED, mask)
    #cv.imshow('a', match)

    #if(minVal_p1 <= 530000):
    #    p1pos = minLoc_p1

    #if(minVal_p2 <= 530000):
    #    p2pos = minLoc_p2

    matches = (np.where(match >= 0.6))
    
    return matches