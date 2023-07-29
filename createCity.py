#!/usr/bin/env python

import matplotlib.pyplot as plt 
from createZones import genZones
from createNodes import genAllNodes
from createHouseholds import genHouseholds
from createLinks import genAllLinks
from convertData import writeFiles
import json
import os
import random
from datetime import datetime

def main():
    os.system("rm -rf ./outputs/")
    os.system("rm -rf ./output/")
    os.system("mkdir ./output/")
    with open('config.json', 'r') as f:
        config = json.loads(f.read())
    
    cityInfo = config['city']
    
    XLENGTH = cityInfo['xLength']
    YLENGTH = cityInfo['yLength']
    AREA = XLENGTH * YLENGTH

    cityDimensions = (XLENGTH, YLENGTH)
 
    zoneInfo = config['zones']

    seeds = config.get("seeds")

    print("Generating zones...")
    zoneRandom = getRandom("zones", seeds)
    cellLength, districts = genZones(cityDimensions, zoneInfo, config.get('subZones'), plt, zoneRandom)
   
    print("Generating nodes in zones...")
    nodeRandom = getRandom("nodes", seeds)
    locations, regions = genAllNodes(zoneInfo, cellLength, plt, config.get('subZones'), nodeRandom)

    print("Generating households with agents...")
    agentsRandom = getRandom("agents", seeds)
    people = genHouseholds(locations, cityInfo, agentsRandom)
   
    print("Generating links between nodes...")
    linksRandom = getRandom("links", seeds)
    links = genAllLinks(config.get('links'), regions, districts, locations, plt, linksRandom)

    del regions, districts
    
    print("Converting data to MATSIM format")
    writeFiles(locations, people, links)

    print("Running MATSIM simulation and generating plot...")
    os.system("java -cp matsim.jar org.matsim.run.RunMatsim matsimConfig.xml&&gunzip outputs/*.gz outputs/ITERS/*/*.gz&")

    plt.legend(loc="upper left")
    plt.show()

def getRandom(mode, seeds):
    currentSeed = datetime.now().timestamp()
    
    if seeds and seeds.get(mode):
        currentSeed = seeds.get(mode)
    
    returnRandom = random.Random(currentSeed)
    
    print(f"The {mode} seed is currently set to {currentSeed}")

    return returnRandom

main()
