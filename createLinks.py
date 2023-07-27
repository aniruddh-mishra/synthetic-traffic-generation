import random
from status import StatusBar

def genAllLinks(linkConfigs, locations, plt, random):
    currentRegion = None
    regionLocations = []
    for location in locations:
        if currentRegion and location.region != currentRegion:
            currentRegion = location.region
            numCentralHubs = 1
            if linkConfigs.get("numCentralHubs"):
                numCentralHubs = random.randint(*linkConfigs.get("numCentralHubs"))
            genInterRegionLinks(numCentralHubs, regionLocations, plt)
            regionLocations = []
        elif location.region != currentRegion:
            currentRegion = location.region
        regionLocations.append(location)
    currentRegion = location.region
    numCentralHubs = 1
    if linkConfigs.get("numCentralHubs"):
        numCentralHubs = random.randint(*linkConfigs.get("numCentralHubs"))
    genInterRegionLinks(numCentralHubs, regionLocations, plt)

def genInterRegionLinks(numCentralHubs, regionNodes, plt):
    numCentralHubs = min(len(regionNodes), numCentralHubs)
    centralHubs = random.sample(regionNodes, numCentralHubs)
    links = []
    for hub in centralHubs:
        for node in regionNodes:
            if node == hub:
                continue
            links.append([node.location, hub.location])
            plt.plot([node.location[0], hub.location[0]], [node.location[1], hub.location[1]], color="black", linewidth=1)

    return links

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json
    from createUniqueZones import genZones
    from createNodes import genAllNodes
    from createHouseholds import genHouseholds
    import random

    with open('config.json', 'r') as f:
        info = json.load(f)

    zoneInfo = info['zones']
    city = info['city']
    dimensions = city['xLength'], city['yLength']

    cellLength = genZones(dimensions, zoneInfo, info.get('subZones'), plt, random)
    print("Generating Nodes...")
    locations = genAllNodes(zoneInfo, cellLength, plt, info.get('subZones'), random)
    
    genAllLinks(info.get('links'), locations, plt, random)

    plt.plot(0, 0)
    plt.legend(loc="upper left")
    plt.show()

"""
def genIntraZoneLinks(nodes, centralHub, plt, counter, centralHubIndex):
    links = []
    for node in nodes:
        if node == centralHub:
            counter += 1
            continue
        dx, dy = [node[0], centralHub[0]], [node[1], centralHub[1]]
        links.append((counter, centralHubIndex))
        plt.plot(dx, dy, color="black", linewidth=1)
        counter += 1
    return links, counter

def genInterZoneLinks(centralHubs, plt):
    links = []
    for hubIndex, hub in enumerate(centralHubs):
        coordinate = hub[0]
        nodeIndex = hub[1]
        if coordinate == centralHubs[-1:][0][0]:
            otherCoordinate = centralHubs[0][0]
            otherNodeIndex = centralHubs[0][1]
            dx, dy = [otherCoordinate[0], coordinate[0]], [otherCoordinate[1], coordinate[1]]
        else:
            otherCoordinate = centralHubs[hubIndex + 1][0]
            otherNodeIndex = centralHubs[hubIndex + 1][1]
            dx, dy = [otherCoordinate[0], coordinate[0]], [otherCoordinate[1], coordinate[1]]
        links.append((nodeIndex, otherNodeIndex))
        plt.plot(dx, dy, color="white", linewidth=1)
    return links

def genAllLinks(method, zones, plt):
    roads = []
    hubs = []
    links = []
    counter = 1
    for zone, info in zones.items():
        nodes = info.get('nodes')
        if not nodes:
            continue
        print(len(nodes.keys()), "areas in zone", zone)
        statusBar = StatusBar(len(nodes.keys()))
        for nodeSet in nodes.values():
            if not nodeSet:
                return
            centralHub = random.choice(nodeSet)
            centralHubIndex = nodeSet.index(centralHub) + counter
            linksResult, counter = genIntraZoneLinks(nodeSet, centralHub, plt, counter, centralHubIndex)
            links.extend(linksResult)
            hubs.append((centralHub, centralHubIndex))
            statusBar.updateProgress()

        statusBar.complete()

    print("Connecting areas with highways...")
    random.shuffle(hubs)
    links.extend(genInterZoneLinks(hubs, plt))
    return links
"""
