extendD = 300
extendL = 200
extendR = 200
extendU  = 100

alphaPos = 0.90
betaPos = 1-alphaPos

alphaScale = 0.90
betaScale = 1-alphaScale


class BoundingBox:
    def __init__(self, pos, width, height):
        self.pos = pos
        self.width = width
        self.height = height

def getBoundingBox(points):
    maxY, maxX = 0,0
    minY, minX = 999999,999999
    for (y, x) in points:
        if x > maxX:
            maxX = x
        if x < minX:
            minX = x
        if y > maxY:
            maxY = y
        if y < minY:
            minY = y

    pos = (minX - extendL, minY - extendU)

    width = maxX - minX + extendR

    height = maxY - minY + extendD

    if height > width :
        width = (height/9)*16
    else:
        height = (width/16)*9

    return BoundingBox(pos, width, height)

def interpolateBoxes(a, b):
    width = a.width*alphaScale+b.width*betaScale
    height = (width/16)*9
    return BoundingBox((a.pos[0]*alphaPos+b.pos[0]*betaPos , a.pos[1]*alphaPos+b.pos[1]*betaPos) , width, height)

def roundCoords(box):
    print(box)
    (x, y) = box.pos
    box.pos = (int(round(x)), int(round(y)))
    box.height = round(box.height)
    box.width = round(box.width)
    return box