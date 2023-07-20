import matplotlib.pyplot as plt 
from createUniqueZones import genZones
from createNodes import genAllNodes

def main():
    cityDimensions = (20000, 20000)
    zoneInfo = {
            'residential': {
                'area': 2092,
                'color': 'red' 
                },
            'industrial': {
                'area': 12000,
                'color': 'orange'
                },
            'commercial': {
                'area': 5000,
                'color': 'green'
                },
            }
    zones = genZones(cityDimensions, zoneInfo.keys(), plt)
    genZoneInfo(zones, zoneInfo)
    genAllNodes(zoneInfo, plt)
    plt.legend()
    plt.show()

def genZoneInfo(zones, zoneInfo):
    for zone, box in zones.items():
        zoneInfo[zone]['box'] = box

main()
