import random
from shapely import Point

def newNode(zoneBounds, occupied):
    minX = zoneBounds[0]
    minY = zoneBounds[1]
    maxX = zoneBounds[2]
    maxY = zoneBounds[3]
    x = random.uniform(minX, maxX)
    y = random.uniform(minY, maxY)
    node = (x, y)
    if node in occupied:
        node = newNode(zoneBounds, occupied)
        return node
    occupied.append(node)
    return node

def genZoneNodes(zone, numNodes, plt, color):
    bounds = zone.bounds
    occupiedNodes = []
    for i in range(numNodes):
        length = len(occupiedNodes)
        if length % 1000 == 0:
            print(length)
        node = newNode(bounds, occupiedNodes)
        plt.plot(*node, marker="o", color=color)
    return occupiedNodes

def genAllNodes(zones, plt):
    zoneNodes = {}
    for zone, info in zones.items():
        zoneBox = info['box']
        area = zoneBox.area
        buildingArea = info['area']
        buildingColor = info['color']
        numNodes = int(area / buildingArea)
        print(zone, numNodes)
        nodes = genZoneNodes(zoneBox, numNodes, plt, buildingColor)
        zoneNodes[zone] = nodes
    return zoneNodes
