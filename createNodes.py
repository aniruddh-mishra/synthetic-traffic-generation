import random
from status import StatusBar
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

def genZoneNodes(land, numNodes, plt, bar):
    zoneNodes = {}
    for area in land:
        occupiedNodes = []
        for i in range(numNodes):
            node = newNode(area, occupiedNodes)
            plt.plot(*node, marker=".", color='white', markersize=1)
            bar.updateProgress()
        zoneNodes[area] = occupiedNodes
    bar.complete()
    return zoneNodes

def genAllNodes(zones, plt):
    for zone, info in zones.items():
        land = info['land']
        if len(land) == 0:
            continue
        sampleArea = land[0]
        area = (sampleArea[2] - sampleArea[0]) ** 2
        buildingArea = info['area']
        numNodes = round(area / buildingArea)
        statusBar = StatusBar(numNodes * len(land))
        print(numNodes * len(land), "nodes in zone", zone)
        nodes = genZoneNodes(land, numNodes, plt, statusBar)
        zones[zone]['nodes'] = nodes
    return zones
