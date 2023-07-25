import matplotlib.pyplot as plt 
from createUniqueZones import genZones
from createNodes import genAllNodes
from createLinks import genAllLinks
from createJobs import genJobs
from createHouseholds import genHouseholds
from convertData import writeFiles
import json
import os
import random

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

    print("Generating zones...")
    genZones(cityDimensions, zoneInfo, plt, random.Random(3))
   
    print("Generating nodes in zones...")
    genAllNodes(zoneInfo, plt)

    print("Generating links between nodes...")
    links = genAllLinks(1, zoneInfo, plt)

    print("Generating jobs within city...")
    jobs = genJobs(zoneInfo)

    print("Generating households with agents...")
    houseHolds = genHouseholds(zoneInfo, jobs, cityInfo['pctWorkFromHome']/100)
    
    if not houseHolds:
     return False

    print("Converting data to MATSIM format")
    writeFiles(zoneInfo, houseHolds, links)
    plt.legend(loc="upper left")
   
    print("Running MATSIM simulation and generating plot...")
    os.system("java -cp matsim.jar org.matsim.run.RunMatsim matsimConfig.xml&")
    plt.show()


main()
