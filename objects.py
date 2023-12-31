class Person:
    def __init__(self, house, job):
        self.house = house
        self.job = job
        self.schedule = []
        self.currentVehicle = None
        self.workFromHome = False

    def getNextAvailable(self):
        timings = [task["times"] for task in self.schedule]
        return timings[-1][1]

    def addToSchedule(self, actionType, location, times, transport):
        task = {
            "actionType": actionType,
            "location": location,
            "times": times,
            "legMode": transport
        }
        self.currentVehicle = transport
        if actionType == "work" and location.location == self.house.location:
            self.workFromHome = True
        self.schedule.append(task)

    def convertToXML(self, id, parentSection, doc):
        attributes = {
            "id": id
        }
        personXML = writeToXML('person', attributes, parentSection, doc)

        plan = doc.createElement('plan')
        personXML.appendChild(plan)

        self.convertScheduleToXML(plan, doc)
        
    def convertScheduleToXML(self, parentSection, doc):
        startOfDay = self.schedule[0]
        leaveHouse = startOfDay["times"][0]
        taskHouse = {
            "actionType": "home",
            "location": self.house,
            "legMode": self.schedule[0]["legMode"],
            "times": [None, leaveHouse]
        }

        self.makeAct(taskHouse, parentSection, doc, not self.workFromHome)
    
        for task in self.schedule:
            if not self.workFromHome or task["actionType"] != "work":
                self.makeAct(task, parentSection, doc, True)

        taskHouse["times"] = None
        self.makeAct(taskHouse, parentSection, doc)

    def makeAct(self, task, parentSection, doc, leg=False):
        actAttributes = {
            "type": task["actionType"],
            "x": task["location"].location[0],
            "y": task["location"].location[1],
        }
        if task.get("times"):
            endTime = task["times"][1]
            endHour = int(endTime)
            endMinute = round((endTime % 1) * 60)
            endTimeString = f"{endHour:02}:{endMinute:02}:00"
            actAttributes["end_time"] = endTime * 3600
        writeToXML('act', actAttributes, parentSection, doc)
        if leg:
            legAttributes = {
                "mode": task["legMode"]
            }
            writeToXML('leg', legAttributes, parentSection, doc)

    def __str__(self):
        returnString = "Here's some information about this person:\n\n\t* This person has the following schedule: \n"
        counter = 0
        for task in self.schedule:
            counter += 1
            returnString += "\t\t" + str(counter) + ". " + task["actionType"] + " located at " + str(task["location"].location) + " from " + str(task["times"][0]) + " to " + str(task["times"][1]) + "\n"
        returnString += "\n\t* This person lives at " + str(self.house.location)
        return returnString + "\n"

class Location:
    def __init__(self, location, locationTypes, zone, region, numResidents=None, maxWorkers=None, houseEquivalence=None):
        self.location = location
        self.locationTypes = locationTypes
        self.zone = zone
        self.region = region
        self.numResidents = numResidents
        self.maxWorkers = maxWorkers
        self.timings = None
        self.houseEquivalence = houseEquivalence
        self.transport = []
        self.workers = []

    def hasCar(self, timings):
        for car in self.transport:
            if self.isCarAvailable(car["times"], timings):
                return True

    def checkoutCar(self, timings):
        for car in self.transport:
            index = 0
            for time in car["times"]:
                if time[0] < timings[0] and time[1] < timings[1]:
                    car["times"].insert(index + 1, timings)
                    return
                index += 1
            if not len(car["times"]):
                car["times"].append(timings)

    def isCarAvailable(self, car, timings):
        for time in car:
            if (time[0] >= timings[0] and time[1] <= timings[1]) or (time[1] >= timings[1] and time[0] <= timings[0]):
                return False
        return True

    def addWorker(self, agent):
        self.workers.append(agent)

    def isHiring(self):
        return not self.maxWorkers or len(self.workers) < self.maxWorkers

    def convertToXML(self, id, parentSection, doc):
        attributes = {
            "id": id,
            "x": self.location[0],
            "y": self.location[1]
        }
        writeToXML('node', attributes, parentSection, doc)

    def __str__(self):
        return f"This node is located at {self.location} and is of the type(s) {', '.join(self.locationTypes)}. It has {self.numResidents} residents and the maximum number of workers here is {self.maxWorkers}. The timings for this location are set to {self.timings}"

class Link:
    def __init__(self, numLanes, speedLimit, modes, capacity, nodes, locations, random):
        self.numLanes = numLanes
        self.speedLimit = speedLimit
        self.modes = modes
        self.capacity = capacity
        self.nodes = nodes
        self.locations = locations
        self.length = self.calcDistance(random)

    def convertToXML(self, id, parentSection, doc):
        attributes = {
            "id": id,
            "from": self.nodes[0] + 1,
            "to": self.nodes[1] + 1,
            "length": self.length,
            "capacity": self.capacity,
            "permlanes": self.numLanes,
            "freespeed": self.speedLimit,
            "modes": self.modes
        }
        writeToXML('link', attributes, parentSection, doc)
        attributes["id"] += 1
        attributes["from"] = self.nodes[1] + 1
        attributes["to"] = self.nodes[0] + 1
        writeToXML('link', attributes, parentSection, doc)

    def calcDistance(self, random):
        nodeOne = self.locations[0].location
        nodeTwo = self.locations[1].location
        deltaX = nodeOne[0] - nodeTwo[0]
        deltaY = nodeOne[1] - nodeTwo[1]
        exactDistance = ((deltaX ** 2) + (deltaY ** 2)) ** 0.5
        addedDistance = random.uniform(0, 0.5) * exactDistance
        return exactDistance + addedDistance

def writeToXML(objectName, attributes, parentSection, doc):
    xmlObject = doc.createElement(objectName)
    for attribute, value in attributes.items():
        xmlObject.setAttribute(attribute, str(value))
    parentSection.appendChild(xmlObject)
    return xmlObject
