import random
from shapely import box
from matplotlib.patches import Rectangle

def genZones(dimensions, zones, plt):
    totalArea = dimensions[0] * dimensions[1]
    minArea = 0
    for zone, info in zones.items():
        if info['area'] > minArea:
            minArea = info['area'] * info['minBuildings']
        zones[zone]['land'] = []
        zones[zone]['landArea'] = zones[zone]['landAreaPct'] * totalArea

    minLength = minArea ** 0.5
    x, y = (0, minLength)
    zoneTypes = list(zones.keys())
    weights = []
    for zone in zoneTypes:
        weights.append(zones[zone]['landArea'])
    while True:
        x += minLength
        if x > dimensions[0]:
            x = minLength
            y += minLength
        if y > dimensions[1] or len(zoneTypes) == 0:
            break
        zone = random.choices(zoneTypes, weights=weights)[0]
        zones[zone]['land'].append((x - minLength, y - minLength, x, y))

        if len(zones[zone]['land']) * minArea > zones[zone]['landArea']:
            index = zoneTypes.index(zone)
            zoneTypes.remove(zone)
            weights.pop(index)
    

    plotZones(minLength, zones, plt)
    return zones

def plotZones(minLength, zones, plt):
    for zone, info in zones.items():
        land = info['land']
        setLegend = True
        for segment in land:
            landBox = box(*segment)
            plt.gca().add_patch(Rectangle(segment[:2], minLength, minLength, facecolor=info['color'], label=zone if setLegend else "__nolegend__"))
            setLegend = False

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    dimensions = (1000, 1000)
    zones = {
            'res': {
                'area': 200,
                'landArea': 200000,
                'color': 'red' 
                },
            'ind': {
                'area': 3000,
                'landArea': 200000,
                'color': 'blue'
                },
            'com': {
                'area': 300,
                'landArea': 2000000,
                'color': 'green'
                }
            }
    genZones(dimensions, zones, plt)
    plt.legend()
    plt.show()
