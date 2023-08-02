from status import StatusBar
from objects import Location

def genAllNodes(zones, cellLength, plt, subZoneInfo, random):
    locations = []
    regions = {}
    statusBar = StatusBar(len(zones.keys()))

    for zone, info in zones.items():
        if info.get('notAlone'):
            continue
        for region in info['land']:
            cellLocations = genCellNodes(region, cellLength, info, plt, subZoneInfo, random, regions, zone)
            locations.extend(cellLocations)
            regions[region] = cellLocations
        statusBar.updateProgress()

    statusBar.complete()

    return locations, regions

def nodeToLocations(node, info, random, zoneType, region):
    numResidents = None
    maxWorkers = None
    if info.get("numResidents"):
        numResidents = random.randint(*info['numResidents'])
    
    if info.get("maxWorkers"):
        maxWorkers = random.randint(*info['maxWorkers'])
    
    location = Location(node, info['buildingTypes'], zoneType, region, numResidents, maxWorkers, info.get("houseEquivalence"))
   
    timings = info.get("timings")
    if timings:
        timingSpecific = {}
        for typeTime, info in timings.items():
            variation = info.get("normalTimeDistribution")
            if not variation:
                variation = 0
           
            start = abs(random.gauss(info["time"][0], variation))
            start = min(info["time"][0] + variation, max(info["time"][0] - variation, start))
            end = abs(random.gauss(info["time"][1], variation))
            end = min(info["time"][1] + variation, max(info["time"][1] - variation, end))
            
            if end < start:
                start = info["time"][0]
                end = info["time"][1]
           
            info = info.copy()
            info["time"] = [start, end]
            timingSpecific[typeTime] = info

        location.timings = timingSpecific
    
    return location

def genCellNodes(region, cellLength, zoneInfo, plt, subZoneInfo, random, regions, zoneType):
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
        if not neighborHasTop(region, regions, zoneType, locations):
            buildingType = "top"

        color = "white"
        buildingInfo = zoneInfo
        if buildingType != "top":
            buildingInfo = subZoneInfo[buildingType]
            color = buildingInfo['color']
        
        if cellArea - coveredArea < buildingInfo['buildingArea']:
            buildingTypes.remove(buildingType)
            continue
      
        coveredArea += buildingInfo['buildingArea']
        
        while True:
            coordinate = (random.uniform(minX, maxX),  random.uniform(minY, maxY))
            if coordinate not in cellNodes:
                break
    
        cellNodes.append(coordinate)
        
        if buildingType == "top":
            buildingType = zoneType
        locations.append(nodeToLocations(coordinate, buildingInfo, random, buildingType, region))
        plt.plot(*coordinate, marker="*", markersize=1, color=color)
   
    return locations

def neighborHasTop(region, regions, topZone, currentLocations):
    neighbors = [(-1, 0), (0, 1), (0, -1), (1, 0)]
    for neighbor in neighbors:
        regionCoordinates = region[0] + neighbor[0], region[1] + neighbor[1]
        locations = regions.get(regionCoordinates)
        if not locations:
            continue
        for location in locations:
            if location.zone == topZone:
                return True
  
    if len(currentLocations):
        for location in currentLocations:
            if location.zone == topZone:
                return True

    return False

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json
    from createZones import genZones
    import random

    with open('config.json', 'r') as f:
        info = json.load(f)

    zoneInfo = info['zones']
    city = info['city']
    dimensions = city['xLength'], city['yLength']

    cellLength, _ = genZones(dimensions, zoneInfo, info.get('subZones'), plt, random)
    print("Generating Nodes...")
    locations, regions = genAllNodes(zoneInfo, cellLength, plt, info.get('subZones'), random)
    for location in locations:
        print(location)
    plt.plot(0, 0)
    plt.legend(loc="upper left")
    plt.show()
