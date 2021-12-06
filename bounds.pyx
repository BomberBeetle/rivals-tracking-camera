import numpy as np
cimport numpy as np
np.import_array()

cdef int extendD = 200
cdef int extendL = 50
cdef int extendR = 50
cdef int extendU  = 50

cdef float alphaPos = 0.90
cdef float betaPos = 1-alphaPos

cdef float alphaScale = 0.90
cdef float betaScale = 1-alphaScale

cdef extern from "bounding_boxes.h":
    struct f_BoundingBox:
        float pos[2]
        float width
        float height

    struct i_BoundingBox:
        int pos[2]
        int width
        int height

class BoundingBox:
    def __init__(self, pos, width, height):
        self.pos = pos
        self.width = width
        self.height = height

cpdef f_BoundingBox getBoundingBox(points: np.ndarray):
    cdef int maxY = 0
    cdef int maxX = 0
    cdef int minY = 999999
    cdef int minX = 999999
    for (y, x, _) in points:
        if x > maxX:
            maxX = x
        if x < minX:
            minX = x
        if y > maxY:
            maxY = y
        if y < minY:
            minY = y

    cdef float posX = minX - extendL
    cdef float posY = minY - extendU

    cdef float midX = (minX+maxX) / 2
    cdef float midY = (minY+maxY) / 2

    cdef float width = maxX - minX +extendL +extendR

    cdef float height = maxY - minY + extendU+ extendD

    cdef float ratioX = (midX - posX)/width
    cdef float ratioY = (midY - posY)/height

    if height/9 > width/16 :
        width = (height/9)*16
        posX -= (height/9)*16*ratioX/2
    else:
        height = (width/16)*9
        posY -= (width/16)*9*ratioY/2



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

    cdef f_BoundingBox bBox
    bBox.pos = [posX, posY]
    bBox.width = width
    bBox.height = height

    return bBox

cpdef f_BoundingBox interpolateBoxes(a: f_BoundingBox, b: f_BoundingBox):
    cdef float width = a.width*alphaScale+b.width*betaScale
    cdef float height = (width/16)*9

    cdef f_BoundingBox bBox
    bBox.pos = [a.pos[0]*alphaPos+b.pos[0]*betaPos , a.pos[1]*alphaPos+b.pos[1]*betaPos]
    bBox.width = width
    bBox.height = height

    return bBox

cpdef i_BoundingBox roundCoords(box: f_BoundingBox):
    cdef int pos[2]
    pos = [int(round(box.pos[0])), int(round(box.pos[1]))]
    cdef int height = round(box.height)
    cdef int width = round(box.width)
    cdef i_BoundingBox bBox
    bBox.pos = pos
    bBox.height = height
    bBox.width = width
    return bBox

cpdef i_BoundingBox get_ibb():
    cdef i_BoundingBox bBox
    return bBox

cpdef f_BoundingBox get_fbb():
    cdef f_BoundingBox bBox
    return bBox