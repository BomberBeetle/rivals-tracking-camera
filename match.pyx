import cv2 as cv
import numpy as np
cimport numpy as np
np.import_array()

cdef np.ndarray template = cv.imread('template_percent.png')
#template = cv.resize(template, (template.shape[0]//2, template.shape[1]//2), interpolation=cv.INTER_NEAREST)
template = cv.cvtColor(template, cv.COLOR_BGR2GRAY) 

cdef np.ndarray mask = cv.imread('template_percent_mask.png')
#mask = cv.resize(mask, (mask.shape[0]//2, mask.shape[1]//2), interpolation=cv.INTER_NEAREST)
mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY) 

cpdef np.ndarray getMatches(frame: np.ndarray, crop_top: int, crop_bottom: int, crop_sides: int):

    frame = cv.resize(frame, (960, 540), interpolation=cv.INTER_NEAREST)
    frame = frame[crop_top:540-crop_bottom,crop_sides:960-crop_sides]
    cdef np.ndarray frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cdef np.ndarray match =cv.matchTemplate(frame_gray, template, cv.TM_CCORR_NORMED, mask)
    #cv.imshow('a', match)

    #if(minVal_p1 <= 530000):
    #    p1pos = minLoc_p1

    #if(minVal_p2 <= 530000):
    #    p2pos = minLoc_p2

    matches = (np.where(match >= 0.6))
    
    return np.column_stack(matches)