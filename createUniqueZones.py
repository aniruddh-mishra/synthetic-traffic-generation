from shapely import box
from status import StatusBar
from matplotlib.patches import Rectangle

def genZones(dimensions, zoneInfo, plt, random):
    cellArea = 0
    zoneTypes = []
    totalPct = 0
    for zone, info in zoneInfo.items():
        if info['area'] > cellArea:
            cellArea = info['area']
        zoneTypes.append(zone)
        info['maxZoneArea'] = info['area'] * info['maxBuildings']
        info['land'] = []
        totalPct += info['landAreaPct']
   
    if totalPct < 1:
        print("Check config.json to make sure all zone percentages add up to 1")
        return

    minLength = cellArea ** 0.5
    xNum = int(dimensions[0] / minLength)
    yNum = int(dimensions[1] / minLength)
    totalArea = dimensions[0] * dimensions[1]

    zones = []
    for y in range(yNum):
        zoneRow = []
        for x in range(xNum):
            zoneRow.append(None)
        zones.append(zoneRow)

    weights = []
    for zone in zoneTypes:
        score = getRemainingCells(zoneInfo[zone], cellArea, totalArea)
        zoneInfo[zone]['maxNumCells'] = max(1, int(zoneInfo[zone]['maxZoneArea'] / cellArea))
        weights.append(score / zoneInfo[zone]['maxNumCells'])

    statusBar = StatusBar(len(zones))
    for rowIndex, row in enumerate(zones):
        for cellIndex, cell in enumerate(row):
            if not cell:
                zoneType = random.choices(zoneTypes, weights=weights)[0]
                numCells = zoneInfo[zoneType]['maxNumCells'] 
                remainingCells = getRemainingCells(zoneInfo[zoneType], cellArea, totalArea)

                if remainingCells < numCells:
                    numCells = remainingCells
                    zoneIndex = zoneTypes.index(zoneType)
                    zoneTypes.remove(zoneType)
                    weights.pop(zoneIndex)

                cells = addCells(numCells, zones, (cellIndex, rowIndex), zoneType, random)
                zoneInfo[zoneType]['land'].extend(cells)
        statusBar.updateProgress()

    statusBar.complete()

    plotZones(minLength, zones, plt, zoneInfo)

def getRemainingCells(zone, cellArea, totalArea):
    totalLand = len(zone['land']) * cellArea
    remainingLand = zone['landAreaPct'] * totalArea - totalLand
    return round(remainingLand / cellArea)

def addCells(numCells, zones, startPoint, zoneType, random):
    cellsAccounted = 1
    reach = 0
    allCells = [startPoint]
    previousAdjacent = None
    while reach < len(zones):
        reach += 1
        adjacentCells = checkAdjacent(zones, startPoint, allCells)
        if not adjacentCells and not previousAdjacent:
            break
        if not adjacentCells:
            adjacentCells = previousAdjacent
        else:
            previousAdjacent = adjacentCells
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

    genZones(dimensions, zoneInfo, plt, random.Random(3))
    plt.plot(*dimensions)
    plt.legend()
    plt.show()
