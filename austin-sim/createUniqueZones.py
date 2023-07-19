import random
from shapely import box
import matplotlib.pyplot as plt

def containsShape(land, shapes):
    for shape in shapes:
        if land.overlaps(shape) or land.contains(shape):
            return shape
    return False

def cutLand(land, shape):
    landBounds = list(land.bounds)
    shapeBounds = shape.bounds
   
    cutLands = []
    for i in range(4):
        testBounds = landBounds.copy()
        testBounds[i] = shapeBounds[(i + 2) % 4]
        cutLands.append(box(*testBounds))
    
    bestArea = 0
    bestLand = None
    for land in cutLands:
        if land.area > bestArea:
            bestLand = land
            bestArea = land.area
    return bestLand

def newLand(land, shapes):
    ogLand = land
    while True:
        shape = containsShape(land, shapes)
        if shape:
            land = cutLand(land, shape)
        else:
            break
    
    if land.area < 100:
        return newLand(ogLand, shapes)

    return land

def createShape(land):
    landBounds = land.bounds
    minX = random.randint(landBounds[0], int((landBounds[2] - landBounds[0])/3) + landBounds[0])
    minY = random.randint(landBounds[1], int((landBounds[3] - landBounds[1])/3) + landBounds[1])
    maxX = random.randint(minX, landBounds[2])
    maxY = random.randint(minY, landBounds[3])
    return box(minX, minY, maxX, maxY)

def genZones(land, zones):
    zoneBoxes = {}
    shapes = []
    remainingArea = land.area
    for zone in zones:
        land = newLand(land, shapes)
        counter = 0
        while True:
            shape = createShape(land)
            if shape.area > remainingArea/(len(zones) - len(shapes) + 5) and shape.area < remainingArea/(len(zones) - len(shapes) + 3) or counter > 100:
                break
            counter += 1

        plt.plot(*shape.exterior.xy, label=zone)
        zoneBoxes[zone] = shape.bounds
        shapes.append(shape)
        remainingArea -= shape.area
        
    return zoneBoxes


if __name__ == "__main__":
    land = box(0, 0, 1000, 1000)
    zones = ['residential', 'industrial', 'commercial']
    print(genZones(land, zones))
    plt.legend()
    plt.show()

