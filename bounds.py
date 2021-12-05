extendD = 150
extendL = 100
extendR = 100
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
    for (y, x, _) in points:
        if x > maxX:
            maxX = x
        if x < minX:
            minX = x
        if y > maxY:
            maxY = y
        if y < minY:
            minY = y

    posX = minX - extendL
    posY = minY - extendU

    width = maxX - minX +extendL +extendR

    height = maxY - minY + extendU+ extendD

    if height/9 > width/16 :
        width = (height/9)*16
        posX -= (height/9)*16/2
    else:
        height = (width/16)*9
        posY -= (width/16)*9/2


    if(width > 960):
        width = 960
    if(height > 540):
            height = 540

    if(posX < 0):
        posX = 0
    elif(posX+width > 960):
        posX =  960 - width

    if(posY < 0):
        posY = 0
    elif(posY + height > 540):
        posY =  540-height

    return BoundingBox((posX, posY), width, height)

def interpolateBoxes(a, b):
    width = a.width*alphaScale+b.width*betaScale
    height = (width/16)*9
    return BoundingBox((a.pos[0]*alphaPos+b.pos[0]*betaPos , a.pos[1]*alphaPos+b.pos[1]*betaPos) , width, height)

def roundCoords(box):
    (x, y) = box.pos
    pos = (int(round(x)), int(round(y)))
    height = round(box.height)
    width = round(box.width)
    return BoundingBox(pos, width, height)