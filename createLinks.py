import random

def genIntraZoneLinks(nodes, centralHub, plt, counter, centralHubIndex):
    links = []
    for node in nodes:
        if node == centralHub:
            counter += 1
            continue
        dx, dy = [node[0], centralHub[0]], [node[1], centralHub[1]]
        links.append((counter, centralHubIndex))
        plt.plot(dx, dy, color="black")
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
        plt.plot(dx, dy, color="white")
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
        for nodeSet in nodes.values():
            centralHub = random.choice(nodeSet)
            centralHubIndex = nodeSet.index(centralHub) + counter
            linksResult, counter = genIntraZoneLinks(nodeSet, centralHub, plt, counter, centralHubIndex)
            links.extend(linksResult)
            hubs.append((centralHub, centralHubIndex))

    random.shuffle(hubs)
    links.extend(genInterZoneLinks(hubs, plt))
    return links
