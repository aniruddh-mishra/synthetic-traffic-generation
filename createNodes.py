import random
from status import StatusBar
from objects import Location

def genAllNodes(zones, cellLength, plt, subZoneInfo):
    locations = []
    for info in zones.values():
        if info.get('notAlone'):
            continue
        for region in info['land']:
            locations.extend(genCellNodes(region, cellLength, info, plt, subZoneInfo))
    
    return locations

def nodeToLocations(node, info):
    # TODO choose timings
    numResidents = None
    maxWorkers = None
    if "housing" in info['buildingTypes']:
        numResidents = random.randint(*info['numResidents'])
    else:
        maxWorkers = random.randint(*info['maxWorkers'])

    location = Location(node, info['buildingTypes'], numResidents, maxWorkers)
    
    return location

def genCellNodes(region, cellLength, zoneInfo, plt, subZoneInfo):
    buildingArea = zoneInfo['buildingArea']
    subZones = zoneInfo.get('subZones')
    
    color = "white"
    buildingTypes = ['top']
    if subZones:
        for subZone in subZones:
            buildingTypes.append(subZone)
    
    cellNodes = []
    locations = []
    minX, minY = region[0] * cellLength, region[1] * cellLength
    maxX, maxY = minX + cellLength, minY + cellLength
    cellArea = cellLength ** 2
    coveredArea = 0

    while coveredArea <= cellArea:
        if not buildingTypes:
            break

        buildingType = random.choice(buildingTypes)
        if len(cellNodes) == 0:
            buildingType = "top"

        buildingInfo = zoneInfo
        if buildingType != "top":
            buildingInfo = subZoneInfo[buildingType]
            color = buildingInfo['color']
        
        coveredArea += buildingInfo['buildingArea']
        if cellArea - coveredArea <= buildingInfo['buildingArea']:
            buildingTypes.remove(buildingType)
        
        while True:
            coordinate = (random.uniform(minX, maxX),  random.uniform(minY, maxY))
            if coordinate not in cellNodes:
                break

        cellNodes.append(coordinate)
        locations.append(nodeToLocations(coordinate, buildingInfo))
        plt.plot(*coordinate, marker="*", markersize=1, color=color)
    
    return locations

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
    locations = genAllNodes(zoneInfo, cellLength, plt, info.get('subZones'))
    for location in locations:
        print(location)
    plt.plot(0, 0)
    plt.legend(loc="upper left")
    plt.show()
