import matplotlib.pyplot as plt 
from createUniqueZones import genZones
from createNodes import genAllNodes
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
    plt.legend(loc="upper left")
    plt.show()
    

main()
