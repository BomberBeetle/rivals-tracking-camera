import cv2 as cv
import match
fn = 0
capture = cv.VideoCapture('r2r.mp4')
while capture.isOpened():
    fn +=1
    _, frame = capture.read()
    cv.imshow('frame', match.getPlayerMatches(frame))
    cv.waitKey(1)