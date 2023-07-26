from shapely import box
from status import StatusBar
from matplotlib.patches import Rectangle

def genZones(dimensions, zones, plt, random):
    totalArea = dimensions[0] * dimensions[1]
    minArea = 0
    for zone, info in zones.items():
        if info['area'] > minArea:
            minArea = info['area'] * info['minBuildings']
        zones[zone]['land'] = []
        zones[zone]['landArea'] = zones[zone]['landAreaPct'] * totalArea

    minLength = minArea ** 0.5
    numBoxes = (dimensions[1] / minLength) * (dimensions[0] / minLength)
    statusBar = StatusBar(numBoxes)

    x, y = (0, minLength)
    zoneTypes = list(zones.keys())
    weights = []
    for zone in zoneTypes:
        weights.append(zones[zone]['landArea'])
    while True:
        x += minLength
        if x > dimensions[0]:
            x = minLength
            y += minLength
        if y > dimensions[1] or len(zoneTypes) == 0:
            break
        zone = random.choices(zoneTypes, weights=weights)[0]
        zones[zone]['land'].append((x - minLength, y - minLength, x, y))

        if len(zones[zone]['land']) * minArea > zones[zone]['landArea']:
            index = zoneTypes.index(zone)
            zoneTypes.remove(zone)
            weights.pop(index)
        statusBar.updateProgress()

    statusBar.complete()

    plotZones(minLength, zones, plt)
    return zones

def genZonesNew(dimensions, zoneInfo, plt, random):
    minArea = 0
    zoneTypes = []
    totalPct = 0
    for zone, info in zoneInfo.items():
        if info['area'] > minArea:
            minArea = info['area']
        zoneTypes.append(zone)
        info['minZoneArea'] = info['area'] * info['minBuildings']
        info['land'] = []
        totalPct += info['landAreaPct']
   
    if totalPct < 1:
        print("Check config.json to make sure all zone percentages add up to 1")
        return

    minLength = minArea ** 0.5
    xNum = int(dimensions[0] / minLength)
    yNum = int(dimensions[1] / minLength)
    totalArea = dimensions[0] * dimensions[1]

    zones = []
    for y in range(yNum):
        zoneRow = []
        for x in range(xNum):
            zoneRow.append(None)
        zones.append(zoneRow)

    for rowIndex, row in enumerate(zones):
        for cellIndex, cell in enumerate(row):
            if not cell:
                zoneType = random.choices(zoneTypes, weights=[getRemainingCells(zoneInfo[zoneType], minArea, totalArea) for zoneType in zoneTypes])[0]
                numCells = max(1, int(zoneInfo[zoneType]['minZoneArea'] / minArea))
               
                remainingCells = getRemainingCells(zoneInfo[zoneType], minArea, totalArea)

                if remainingCells < numCells:
                    numCells = remainingCells
                    zoneTypes.remove(zoneType)

                cells = addCells(numCells, zones, (cellIndex, rowIndex), zoneType)
                zoneInfo[zoneType]['land'].extend(cells)
   
    plotZones(minLength, zones, plt, zoneInfo)

def getRemainingCells(zone, minArea, totalArea):
    totalLand = len(zone['land']) * minArea
    remainingLand = zone['landAreaPct'] * totalArea - totalLand
    return round(remainingLand / minArea)

def addCells(numCells, zones, startPoint, zoneType):
    cellsAccounted = 1
    reach = 0
    allCells = [startPoint]
    while reach < len(zones):
        reach += 1
        adjacentCells = checkAdjacent(zones, startPoint, allCells)
        if not adjacentCells:
            break
        if len(adjacentCells) > numCells - len(allCells):
            allCells.extend(adjacentCells[:numCells - len(allCells)])
            break
        allCells.extend(adjacentCells)
        startPoint = random.choice(adjacentCells)
    
    for cell in allCells:
        zones[cell[1]][cell[0]] = zoneType

    return allCells

def checkAdjacent(zones, startPoint, usedCells):
    adjacentCells = []
    for deltaX in range(-1, 2):
        for deltaY in range(-1, 2):
            x = startPoint[0] + deltaX
            y = startPoint[1] + deltaY
            zoneAvailable = y >= 0 and x >= 0 and y < len(zones) and x < len(zones[0]) and not zones[y][x] and (x, y) not in usedCells
            zoneDiagonal = (deltaX == -1 or deltaX == 1) and deltaY != 0
            if not zoneAvailable or zoneDiagonal:
                continue
            adjacentCells.append((x, y))
    
    return adjacentCells

def plotZones(minLength, zones, plt, zonesInfo):
    labeledZones = []
    for rowIndex, row in enumerate(zones):
        for cellIndex, cell in enumerate(row):
            startPoint = (cellIndex * minLength, rowIndex * minLength)
            setLegend = True
            if cell in labeledZones:
                setLegend = False
            labeledZones.append(cell)
            plt.gca().add_patch(Rectangle(startPoint, minLength, minLength, facecolor=zonesInfo[cell]['color'], label=cell if setLegend else "__nolegend__"))

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json
    import random 

    with open('config.json', 'r') as f:
        info = json.load(f)

    zoneInfo = info['zones']
    city = info['city']
    dimensions = city['xLength'], city['yLength']

    genZonesNew(dimensions, zoneInfo, plt, random)
    plt.plot(*dimensions)
    plt.legend()
    plt.show()
