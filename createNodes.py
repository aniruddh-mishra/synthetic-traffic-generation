import random
from status import StatusBar
from objects import Location

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

def genAllNodesNew(zones, cellLength, plt):
    locations = []
    for info in zones.values():
        if info.get('notAlone'):
            continue
        for region in info['land']:
            nodes = genCellNodes(region, cellLength, info['buildingArea'], plt)
            locations.extend(nodesToLocations(nodes, info))
    
    return locations

def nodesToLocations(nodes, zoneInfo):
    locations = []
    for node in nodes:
        if zoneInfo.get('subZones'):
            pass # TODO make locations for subzone as well
        
        numResidents = None
        maxWorkers = None
        if "housing" in zoneInfo['types']:
            numResidents = random.randint(*zoneInfo['numResidents'])
        else:
            maxWorkers = random.randint(*zoneInfo['maxWorkers'])

        location = Location(node, zoneInfo['types'], numResidents, maxWorkers)
        locations.append(location)

    return locations

def genCellNodes(region, cellLength, buildingArea, plt):
    cellNodes = []
    minX, minY = region[0] * cellLength, region[1] * cellLength
    maxX, maxY = minX + cellLength, minY + cellLength
    cellArea = cellLength ** 2
    numNodes = int(cellArea / buildingArea)
    for _ in range(numNodes):
        while True:
            coordinate = (random.uniform(minX, maxX),  random.uniform(minY, maxY))
            if coordinate not in cellNodes:
                break
        cellNodes.append(coordinate)
        plt.plot(*coordinate, marker="*", markersize=1, color="white")
    return cellNodes

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json
    from createUniqueZones import genZones

    with open('config.json', 'r') as f:
        info = json.load(f)

    zoneInfo = info['zones']
    city = info['city']
    dimensions = city['xLength'], city['yLength']

    cellLength = genZones(dimensions, zoneInfo, info.get('subZones'), plt, random.Random(3))
    locations = genAllNodesNew(zoneInfo, cellLength, plt)
    for location in locations:
        print(location)
    plt.plot(0, 0)
    plt.legend(loc="upper left")
    plt.show()
