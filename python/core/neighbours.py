from dimensions import Dim2D
from shapes import *
from boundaryChecks import *
from utils import *

def getNeighbours2D_rectangle_4Sides(position):
    checkType(position, Dim2D)
    x, y = position.x, position.y
    candidates = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    candidates = Dim2D.listToDim2Ds(candidates)
    return candidates

def getNeighbours2D_rectangle_8Sides(position):
    checkType(position, Dim2D)
    x, y = position.x, position.y
    candidates = [
        (x+1, y), (x-1, y), (x, y+1), (x, y-1),
        (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
        ]
    candidates = Dim2D.listToDim2Ds(candidates)
    return candidates

def getAvailableNeighbours2D_rectangle(map, blockingPositions, getNeighboursFunction, position):
    checkType(map, Rectangle)
    checkType(blockingPositions, list)
    if blockingPositions:
        checkType(blockingPositions[0], Dim2D)
    checkType(position, Dim2D)
    candidates = getNeighboursFunction(position)

    for candi in reversed(candidates):
        isInsideBoundary = boundaryChecks2D_rectangle(map, candi)
        if not isInsideBoundary:
            candidates.remove(candi)
        elif candi in blockingPositions:
            candidates.remove(candi)
    
    return candidates

def getNeighbours2D_hexagon(position):
    pass