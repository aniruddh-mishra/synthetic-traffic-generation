import matplotlib.pyplot as plt 
from createUniqueZones import genZones
from createNodes import genAllNodes
from createLinks import genAllLinks
from createJobs import genJobs
from createHouseholds import genHouseholds
from convertData import writeFiles
import json
import os

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

    genZones(cityDimensions, zoneInfo, plt)
    genAllNodes(zoneInfo, plt)
    links = genAllLinks(1, zoneInfo, plt)
    jobs = genJobs(zoneInfo)
    houseHolds = genHouseholds(zoneInfo, jobs)
    if not houseHolds:
     return False
    writeFiles(zoneInfo, houseHolds, links)
    plt.legend(loc="upper left")
    
    os.system("java -cp matsim.jar org.matsim.run.RunMatsim matsimConfig.xml&")
    plt.show()


main()
