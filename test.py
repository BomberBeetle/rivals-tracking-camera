import cv2 as cv
import match
fn = 0
capture = cv.VideoCapture('clip2.mp4')
while capture.isOpened():
    fn +=1
    _, frame = capture.read()

    xs,ys = match.getMatches(frame)
    frame = cv.resize(frame, (960, 540), interpolation=cv.INTER_NEAREST)

    frame = frame[40:500,:]

    for (x, y) in zip(xs, ys):
        cv.circle(frame, (y,x), 5, (0,0,255), 2)

    cv.imshow('cringe detector', frame)
    cv.waitKey(16)