import matplotlib.pyplot as plt 
from createUniqueZones import genZones
from createNodes import genAllNodes
from createLinks import genAllLinks
from createJobs import genJobs
from createHouseholds import genHouseholds
import json

def main():
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
    genAllLinks(1, zoneInfo, plt)
    jobs = genJobs(zoneInfo)
    houses = genHouseholds(zoneInfo, jobs)
    if not houses:
     return False
    plt.legend(loc="upper left")
    plt.show()
    
main()
