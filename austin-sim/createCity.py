import matplotlib.pyplot as plt 
from createUniqueZones import genZones
from createNodes import genAllNodes

def main():
    XLENGTH = 4500
    YLENGTH = 4500
    AREA = XLENGTH * YLENGTH

    cityDimensions = (XLENGTH, YLENGTH)
    zoneInfo = {
            'residential': {
                'area': 2092,
                'landArea': 0.75 * AREA,
                'minBuildings': 100,
                'color': 'red' 
                },
            'industrial': {
                'area': 12000,
                'landArea': 0.15 * AREA,
                'minBuildings': 100,
                'color': 'orange'
                },
            'commercial': {
                'area': 5000,
                'landArea': 0.1 * AREA,
                'minBuildings': 90,
                'color': 'green'
                },
            }
    genZones(cityDimensions, zoneInfo, plt)
    genAllNodes(zoneInfo, plt)
    plt.legend(loc="upper left")
    plt.show()

main()
