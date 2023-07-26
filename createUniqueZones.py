from shapely import box
from status import StatusBar
from matplotlib.patches import Rectangle

def genZones(dimensions, zoneInfo, subZones, plt, random):
    cellArea = 0
    zoneTypes = []
    totalPct = 0

    for info in subZones.values():
        if info['buildingArea'] > cellArea:
            cellArea = info['buildingArea']

    for zone, info in zoneInfo.items():
        if info['buildingArea'] > cellArea:
            cellArea = info['buildingArea']

        zoneTypes.append(zone)
        info['maxZoneArea'] = info['buildingArea'] * info['maxBuildings']
        info['land'] = []
        totalPct += info['landAreaPct']
   
    if totalPct < 1:
        print("Check config.json to make sure all zone percentages add up to 1")
        return

    cellLength = cellArea ** 0.5
    xNum = int(dimensions[0] / cellLength)
    yNum = int(dimensions[1] / cellLength)
    totalCells = xNum * yNum

    zones = []
    for y in range(yNum):
        zoneRow = []
        for x in range(xNum):
            zoneRow.append(None)
        zones.append(zoneRow)

    statusBar = StatusBar(len(zones))
    for rowIndex, row in enumerate(zones):
        for cellIndex, cell in enumerate(row):
            if not cell:
                weights = [] 
                for zone in zoneTypes:
                    remainingCells = getRemainingCells(zoneInfo[zone], totalCells)
                    zoneInfo[zone]['maxNumCells'] = max(1, int(zoneInfo[zone]['maxZoneArea'] / cellArea))
                    weights.append(remainingCells / zoneInfo[zone]['maxNumCells'])
                
                zoneType = random.choices(zoneTypes, weights=weights)[0]
                numCells = zoneInfo[zoneType]['maxNumCells']
                
                if remainingCells < numCells:
                    numCells = remainingCells
                    zoneTypes.remove(zoneType)

                cells = addCells(numCells, zones, (cellIndex, rowIndex), zoneType, random)
                zoneInfo[zoneType]['land'].extend(cells)
        statusBar.updateProgress()

    statusBar.complete()

    plotZones(cellLength, zones, plt, zoneInfo)
    return cellLength

def getRemainingCells(zone, totalCells):
    remainingCells = zone['landAreaPct'] * totalCells
    return round(remainingCells)

def addCells(numCells, zones, startPoint, zoneType, random):
    cellsAccounted = 1
    reach = 0
    allCells = [startPoint]
    previousAdjacent = None
    while reach < len(zones):
        reach += 1
        adjacentCells = checkAdjacent(zones, startPoint, allCells)
        if not len(adjacentCells) and not previousAdjacent:
            break
        if not len(adjacentCells):
            adjacentCells = previousAdjacent
            continue
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

def plotZones(cellLength, zones, plt, zonesInfo):
    labeledZones = []
    for rowIndex, row in enumerate(zones):
        for cellIndex, cell in enumerate(row):
            startPoint = (cellIndex * cellLength, rowIndex * cellLength)
            setLegend = True
            if cell in labeledZones:
                setLegend = False
            labeledZones.append(cell)
            plt.gca().add_patch(Rectangle(startPoint, cellLength, cellLength, facecolor=zonesInfo[cell]['color'], label=cell if setLegend else "__nolegend__"))

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json
    import random 

    with open('config.json', 'r') as f:
        info = json.load(f)

    zoneInfo = info['zones']
    city = info['city']
    dimensions = city['xLength'], city['yLength']

    genZones(dimensions, zoneInfo, info.get('subZones'), plt, random.Random(3))
    plt.plot(0, 0)
    plt.legend()
    plt.show()
