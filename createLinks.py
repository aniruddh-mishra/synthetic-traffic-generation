import random
from status import StatusBar
from objects import Link

def genAllLinks(linkConfigs, regions, districts, locations, plt, random):
    if not linkConfigs:
        linkConfigs = {}

    numCentralHubs = linkConfigs.get("numCentralHubs")
    allCentralHubs = []
    districtRoads = []
    statusBar = StatusBar(len(districts) +  1)
    for district in districts:
        districtNodes = [] 
        for region in district:
            districtNodes.extend(regions[region])
        intraDistrictRoads, centralHubs = genIntraDistrictLinks(numCentralHubs, districtNodes, plt, random)
        districtRoads.extend(intraDistrictRoads)
        allCentralHubs.extend(centralHubs)
        statusBar.updateProgress()

    highways = findMinimumSpanningTree(allCentralHubs)
    for highway in highways:
        if highway in districtRoads or [highway[1], highway[0]] in districtRoads:
            highways.remove(highway)
    statusBar.updateProgress()
    statusBar.complete()

    plotRoads(highways, "white", plt)

    allRoads = []
    for road in districtRoads:
        numLanes = 1
        speedLimit = 60
        modes = "car"
        capacity = 100
        nodes = [locations.index(road[0]), locations.index(road[1])]
        roadObject = Link(numLanes, speedLimit, modes, capacity, nodes, road)
        allRoads.append(roadObject)

    for road in highways:
        numLanes = 1
        speedLimit = 60
        modes = "car"
        capacity = 1000
        nodes = [locations.index(road[0]), locations.index(road[1])]
        roadObject = Link(numLanes, speedLimit, modes, capacity, nodes, road)
        allRoads.append(roadObject)

    return allRoads

def genIntraDistrictLinks(numCentralHubs, districtNodes, plt, random):
    if len(districtNodes) == 1:
        return [], districtNodes 

    if not numCentralHubs:
        numCentralHubs = 2
    else:
        numCentralHubs = random.randint(*numCentralHubs)
    
    numCentralHubs = max(2, min(numCentralHubs, len(districtNodes)))

    centralHubs = random.sample(districtNodes, numCentralHubs)

    districtRoads = findMinimumSpanningTree(districtNodes)
    plotRoads(districtRoads, "black", plt)
    return districtRoads, centralHubs

def plotRoads(roads, color, plt):
    for road in roads:
        deltaX = [road[0].location[0], road[1].location[0]]
        deltaY = [road[0].location[1], road[1].location[1]]
        plt.plot(deltaX, deltaY, color=color, linewidth=1)

def findMinimumSpanningTree(vertices):
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
    edgeIndex = 0
    while len(treeEdges) < len(vertices) - 1 and edgeIndex < len(edges):
        start, end, distance = edges[edgeIndex]
        edgeIndex += 1
        startParent = findParent(parents, start)
        endParent = findParent(parents, end)

        if startParent != endParent:
            edgeIndex += 1
            treeEdges.append([vertices[start], vertices[end]])
            if ranks[startParent] > ranks[endParent]:
                parents[endParent] = startParent
            elif ranks[startParent] < ranks[endParent]:
                parents[startParent] = endParent
            else:
                parents[startParent] = endParent
                ranks[endParent] += 1

    return treeEdges 

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
