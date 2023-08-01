from status import StatusBar
from objects import Link

def genAllLinks(linkConfigs, regions, districts, locations, plt, random):
    if not linkConfigs:
        linkConfigs = {}

    meshingRatio = linkConfigs.get("meshingRatio")
    allCentralHubs = []
    districtRoads = []
    statusBar = StatusBar(len(districts) +  1)
    for district in districts:
        districtNodes = [] 
        for region in district:
            districtNodes.extend(regions[region])
        intraDistrictRoads, centralHubs = genIntraDistrictLinks(linkConfigs, districtNodes, plt, random)
        districtRoads.extend(intraDistrictRoads)
        allCentralHubs.extend(centralHubs)
        statusBar.updateProgress()

    highways, meshHighways = findMinimumSpanningTree(allCentralHubs, random, meshingRatio)
    highways.extend(meshHighways)
    for highway in highways:
        if highway in districtRoads or [highway[1], highway[0]] in districtRoads:
            highways.remove(highway)
    statusBar.updateProgress()
    statusBar.complete()

    plotRoads(highways, "white", plt)

    districtRoadsCount = 0
    districtRoadsLanes = 0
    totalDistrictSpeedLimit = 0
    districtRoadsDistance = 0

    allRoads = []
    districtRoadConfigs = linkConfigs.get("districtRoads")
    publicTransportRatio = linkConfigs.get("roadsPublicTransportRatio")
    publicTransportSeperate = linkConfigs.get("publicTransportSeperate")
    for road in districtRoads: 
        numLanes = random.randint(*districtRoadConfigs["numLanes"])
        speedLimit = random.randint(*districtRoadConfigs["speedLimit"])
        modes = "car"
        capacity = random.randint(*districtRoadConfigs["capacity"])
        nodes = [locations.index(road[0]), locations.index(road[1])]

        if publicTransportSeperate:
            roadObject = Link(1, speedLimit, "pt", capacity, nodes, road, random)
            districtRoadsLanes += 2
        else:
            modes += ", pt"

        roadObject = Link(numLanes, speedLimit, modes, capacity, nodes, road, random)
        districtRoadsDistance += roadObject.length
        districtRoadsCount += 1
        districtRoadsLanes += numLanes * 2
        totalDistrictSpeedLimit += speedLimit

        allRoads.append(roadObject)

    print(f"{districtRoadsCount} district roads constructed with a total of {districtRoadsLanes} lanes amongst all roads or an average of {round(districtRoadsLanes/districtRoadsCount, 2)} lanes per road. The average district roads speed limit was {round(totalDistrictSpeedLimit/districtRoadsCount, 2)} meters/sec. The total length of road is {round(districtRoadsDistance, 2)} meters.")

    highwaysCount = 0 
    highwaysLanes = 0
    highwaysDistance = 0
    totalSpeedLimit = 0
    highwayConfigs = linkConfigs.get("highways")
    for road in highways:
        numLanes = random.randint(*highwayConfigs["numLanes"])
        speedLimit = random.randint(*highwayConfigs["speedLimit"])
        modes = "car"
        capacity = random.randint(*highwayConfigs["capacity"])                
        nodes = [locations.index(road[0]), locations.index(road[1])]
        if publicTransportSeperate:
            roadObject = Link(1, speedLimit, "pt", capacity, nodes, road, random)
            highwaysLanes += 2
        else:
            modes += ", pt"

        roadObject = Link(numLanes, speedLimit, modes, capacity, nodes, road, random)
        highwaysCount += 1
        highwaysLanes += numLanes * 2
        totalSpeedLimit += speedLimit
        highwaysDistance += roadObject.length
        allRoads.append(roadObject)
    
    print(f"{highwaysCount} highways constructed with a total of {highwaysLanes} lanes amongst all roads or an average of {round(districtRoadsLanes/highwaysCount, 2)} lanes per road. The average highway speed limit was {round(totalSpeedLimit/highwaysCount, 2)} meters/sec. The total length of road is {round(highwaysDistance, 2)} meters.")
    
    return allRoads

def genIntraDistrictLinks(linkConfigs, districtNodes, plt, random):
    numCentralHubs = linkConfigs.get("numCentralHubs")
    meshingRatio = linkConfigs.get("meshingRatio")
    if len(districtNodes) == 1:
        return [], districtNodes 

    if not numCentralHubs:
        numCentralHubs = 2
    else:
        numCentralHubs = random.randint(*numCentralHubs)
    
    numCentralHubs = max(2, min(numCentralHubs, len(districtNodes)))

    centralHubs = random.sample(districtNodes, numCentralHubs)

    districtRoads, meshRoads = findMinimumSpanningTree(districtNodes, random, meshingRatio)
    districtRoads.extend(meshRoads)
    plotRoads(districtRoads, "black", plt)
    return districtRoads, centralHubs

def plotRoads(roads, color, plt):
    for road in roads:
        deltaX = [road[0].location[0], road[1].location[0]]
        deltaY = [road[0].location[1], road[1].location[1]]
        plt.plot(deltaX, deltaY, color=color, linewidth=1)

def findMinimumSpanningTree(vertices, random, meshingRatio):
    if len(vertices) == 1:
        return []

    edges = []
    startIndex = 0
    for start in vertices:
        endIndex = startIndex + 1
        for end in vertices[startIndex + 1: ]:
            edges.append([startIndex, endIndex, pythagoreanTheorem(start.location, end.location)])
            endIndex += 1
        startIndex += 1

    edges.sort(key=lambda edge: edge[2])

    parents = []
    ranks = []
    nodes = []
    for vertexIndex, _ in enumerate(vertices):
        parents.append(vertexIndex)
        ranks.append(0)
        nodes.append(vertexIndex)

    treeEdges = []
    meshEdges = []
    edgeIndex = 0
    while len(treeEdges) < len(vertices) - 1 and edgeIndex < len(edges):
        start, end, distance = edges[edgeIndex]
        edgeIndex += 1
        startParent = findParent(parents, start)
        endParent = findParent(parents, end)

        if startParent != endParent:
            treeEdges.append([vertices[start], vertices[end]])
            if ranks[startParent] > ranks[endParent]:
                parents[endParent] = startParent
            elif ranks[startParent] < ranks[endParent]:
                parents[startParent] = endParent
            else:
                parents[startParent] = endParent
                ranks[endParent] += 1
        else:
            meshEdges.append(edges[edgeIndex])
    
    meshEdges.extend(edges[edgeIndex:])
    meshEdges = random.choices(meshEdges, k=min(int(len(treeEdges) * meshingRatio), len(meshEdges)))
    
    returnMeshes = []
    for edge in meshEdges:
        returnMeshes.append([vertices[edge[0]], vertices[edge[1]]])

    return treeEdges, returnMeshes

def findParent(parents, node):
    if parents[node] == node:
        return node
    return findParent(parents, parents[node])
            
def pythagoreanTheorem(coordinateOne, coordinateTwo):
    deltaX = coordinateOne[0] - coordinateTwo[0]
    deltaY = coordinateOne[1] - coordinateTwo[1]
    return ((deltaX ** 2) + (deltaY ** 2)) ** 0.5

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json
    from createZones import genZones
    from createNodes import genAllNodes
    from createHouseholds import genHouseholds
    import random

    with open('config.json', 'r') as f:
        info = json.load(f)

    zoneInfo = info['zones']
    city = info['city']
    dimensions = city['xLength'], city['yLength']

    cellLength, districts = genZones(dimensions, zoneInfo, info.get('subZones'), plt, random)
    print("Generating Nodes...")
    locations, regions = genAllNodes(zoneInfo, cellLength, plt, info.get('subZones'), random)
   
    print("Generating Links...")
    genAllLinks(info.get('links'), regions, districts, locations, plt, random)

    plt.plot(0, 0)
    plt.legend(loc="upper left")
    plt.show()
