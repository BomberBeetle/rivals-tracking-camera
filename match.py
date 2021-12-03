import cv2 as cv

template = cv.imread('template_p1.png')
template = cv.resize(template, (7,6), interpolation=cv.INTER_NEAREST)
template = cv.cvtColor(template, cv.COLOR_BGR2HSV)

mask = cv.imread('mask.png')
mask = cv.resize(mask, (7,6), interpolation=cv.INTER_NEAREST)

def getPlayerMatches(frame):
    frame = cv.resize(frame, (480, 270), interpolation=cv.INTER_NEAREST)
    frame = frame[40:230, 40:440]
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    match =cv.matchTemplate(frame, template, cv.TM_CCORR_NORMED, mask)
    _,_,_,maxLoc  = cv.minMaxLoc(match)
    return cv.circle(match, maxLoc, 5,255 ,-1)
    