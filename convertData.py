from xml.dom import minidom
import random
from status import StatusBar

def writeFiles(zoneInfo, households, links):
    createNetwork(zoneInfo, links)
    createPopulation(households)

def createPopulation(households):
    populationDoc = minidom.parseString('<?xml version="1.0" ?><!DOCTYPE plans SYSTEM "http://www.matsim.org/files/dtd/plans_v4.dtd"><plans xml:lang="de-CH"></plans>')

    population = populationDoc.childNodes[1]

    numPeople = 0
    print(len(households), "houses to convert...")
    statusBar = StatusBar(len(households))
    for house in households:
        members = house.members
        for person in members:
            numPeople += 1
            person = createPerson(person, populationDoc, numPeople)
            population.appendChild(person)
        statusBar.updateProgress()
    statusBar.complete()

    writeFile(populationDoc, "plans.xml")

def createPerson(person, doc, numPeople):
    personXML = doc.createElement('person')
    attributes = {
        "id": numPeople,
    }
    setAttributes(personXML, attributes)
    
    plan = doc.createElement("plan")
    personXML.appendChild(plan)

    # TODO Change completely
    createAct("home", person.house.location, plan, doc, "car", person.getLeaveHomeTime())
    createAct("work", person.work.location, plan, doc, "car", person.getLeaveWorkTime())
    createAct("home", person.house.location, plan, doc)
    return personXML

def createAct(actType, location, planSection, doc, leg=None, endTime=None):
    action = doc.createElement('act')
    attributes = {
        "type": actType,
        "x": location[0],
        "y": location[1]
    }
    if endTime:
        attributes["end_time"] = endTime
    setAttributes(action, attributes)
    planSection.appendChild(action)
    if leg:
        legXML = doc.createElement('leg')
        attributes = {
            "mode": leg
        }
        setAttributes(legXML, attributes)
        planSection.appendChild(legXML)

def createNetwork(zoneInfo, links):
    networkName = "synthetic city network"
    networkDoc = minidom.parseString(f'<?xml version="1.0" encoding="utf-8"?><!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v1.dtd"><network name="{networkName}"></network>')

    network = networkDoc.childNodes[1]

    nodesSection = networkDoc.createElement('nodes')
    network.appendChild(nodesSection)

    numNodes = 0
    allNodes = []
    for zone, info in zoneInfo.items():
        if not info.get('nodes'):
            continue
        numNodes, nodesResult = createNodes(info["nodes"], nodesSection, numNodes, networkDoc)
        allNodes.extend(nodesResult)

    linksSection = networkDoc.createElement('links')
    network.appendChild(linksSection)

    numLinks = 1
    print(len(links), "links to create")
    statusBar = StatusBar(len(links))
    for link in links:
        createLink(link, linksSection, numLinks, networkDoc, allNodes)
        numLinks +=1
        createLink([link[1], link[0]], linksSection, numLinks, networkDoc, allNodes)
        numLinks += 1
        statusBar.updateProgress()
    statusBar.complete()
    
    writeFile(networkDoc, "network.xml")

def createLink(link, linksSection, numLinks, doc, allNodes):
    linkXML = doc.createElement("link")
    startNode = allNodes[link[0] - 1]
    endNode = allNodes[link[1] - 1]
    distance = calcDistance(startNode, endNode)
    attributes = {
        "id": numLinks,
        "from": link[0],
        "to": link[1],
        "length": distance,
        "capacity": 1800,
        "permlanes": 1,
        "freespeed": 27.8
    }
    setAttributes(linkXML, attributes)
    linksSection.appendChild(linkXML)

def calcDistance(nodeOne, nodeTwo):
    deltaX = nodeOne[0] - nodeTwo[0]
    deltaY = nodeOne[1] - nodeTwo[1]
    distance = (deltaX ** 2 + deltaY ** 2) ** 0.5
    distance *= (1 + random.uniform(0, 0.4))
    return distance

def createNodes(nodes, nodesSection, numNodes, doc):
    allNodes = []
    for nodesArea in nodes.values():
        for node in nodesArea:
            numNodes += 1
            nodeXML = doc.createElement('node')
            attributes = {
                "id": numNodes,
                "x": node[0],
                "y": node[1]
            }
            allNodes.append(node)
            setAttributes(nodeXML, attributes)
            nodesSection.appendChild(nodeXML)
    return numNodes, allNodes

def setAttributes(xmlData, attributes):
    for attribute, value in attributes.items():
        xmlData.setAttribute(attribute, str(value))

def writeFile(file, name):
    with open("output/" + name, "w") as f:
        f.write(file.toprettyxml(indent="\t"))
