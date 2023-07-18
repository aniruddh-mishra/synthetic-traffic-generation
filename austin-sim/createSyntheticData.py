from xml.dom import minidom
import random

doc = minidom.Document()

network = doc.createElement('network')
network.setAttribute('name', 'austin city network')
doc.appendChild(network)

nodes = doc.createElement('nodes')

for i in range(1, 101):
    coordinate = (random.randint(-1000, 1000), random.randint(-1000, 1000))
    node = doc.createElement('node')
    node.setAttribute('id', str(i))
    node.setAttribute('x', str(coordinate[0]))
    node.setAttribute('y', str(coordinate[1]))
    nodes.appendChild(node)

network.appendChild(nodes)

links = doc.createElement('links')

j = 1
for i in range(1, 51):
    link = doc.createElement('link')
    attributes = {
            'id': str(i),
            'from': str(j),
            'to': str(j + 1),
            'length': str(random.randint(1000, 5000)),
            'capacity': str(random.randint(1000, 3000)),
            'freespeed': str(random.randint(60, 100)),
            'permlanes': str(random.randint(1, 4)),
            'modes': 'car'
            }
    for attribute, value in attributes.items():
        link.setAttribute(attribute, value)

    links.appendChild(link)

    j += 2

network.appendChild(links)

with open("data/network.xml", "w") as f:
    f.write(doc.toprettyxml(indent="\t"))

plans = minidom.Document()

population = plans.createElement('population')
plans.appendChild(population)

def createAct():
    types = ["home", "work"]
    coordinate = (random.randint(-1000, 1000), random.randint(-1000, 1000))
    act = plans.createElement('act')
    act.setAttribute('type', random.choice(types))
    act.setAttribute('x', str(coordinate[0]))
    act.setAttribute('y', str(coordinate[1]))
    return act

for i in range(1, 1001):
    person = plans.createElement('person')
    person.setAttribute('id', str(i))

    plan = plans.createElement('plan')
    
    acts = []
    for i in range(24):
        if random.randint(0, 23) <= 2:
            act = createAct()
            act.setAttribute('end_time', "{:02d}".format(i) + ":00:00")
            acts.append(act)

    if len(acts) != 0:
        plan.appendChild(acts[0])
        for act in acts[1:]:
            leg = plans.createElement('leg')
            leg.setAttribute('mode', 'car')
            plan.appendChild(leg)
            plan.appendChild(act)

    person.appendChild(plan)
    population.appendChild(person)

with open("data/plans.xml", "w") as f:
    f.write(plans.toprettyxml(indent="\t"))

