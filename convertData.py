from xml.dom import minidom
from status import StatusBar

def writeFiles(locations, people, links):
    createNetwork(locations, links)
    createPopulation(people)

def createPopulation(people):
    populationDoc = minidom.parseString('<?xml version="1.0" ?><!DOCTYPE plans SYSTEM "http://www.matsim.org/files/dtd/plans_v4.dtd"><plans xml:lang="de-CH"></plans>')

    population = populationDoc.childNodes[1]

    personId = 1
    print("Writing Agents...")
    statusBar = StatusBar(len(people))
    for person in people:
        person.convertToXML(personId, population, populationDoc)
        personId += 1
        statusBar.updateProgress()
    statusBar.complete()

    writeFile(populationDoc, "plans.xml")

def createNetwork(locations, links):
    networkName = "synthetic city network"
    networkDoc = minidom.parseString(f'<?xml version="1.0" encoding="utf-8"?><!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v1.dtd"><network name="{networkName}"></network>')

    network = networkDoc.childNodes[1]

    nodesSection = networkDoc.createElement('nodes')
    network.appendChild(nodesSection)

    print("Writing Nodes...")
    statusBar = StatusBar(len(locations))
    nodeId = 1
    for location in locations:
        location.convertToXML(nodeId, nodesSection, networkDoc)
        nodeId += 1
        statusBar.updateProgress()

    statusBar.complete()

    linksSection = networkDoc.createElement('links')
    network.appendChild(linksSection)

    linkId = 1
    print("Writing Links...")
    statusBar = StatusBar(len(links))
    for link in links:
        link.convertToXML(linkId, linksSection, networkDoc)
        linkId += 2
        statusBar.updateProgress()

    statusBar.complete()
    
    writeFile(networkDoc, "network.xml")

def writeFile(file, name):
    with open("output/" + name, "w") as f:
        f.write(file.toprettyxml(indent="\t"))
