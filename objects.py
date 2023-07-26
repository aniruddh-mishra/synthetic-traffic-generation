import random

class Person:
    def __init__(self, house, work):
        self.house = house
        self.work = work

    def setLeaveHomeTime(timeRange):
        self.endTimeHome = pickTime(timeRange)

    def setLeaveWorkTime(timeRange):
        self.endTimeWork = pickTime(timeRange)
        if self.endTimeHome > self.endTimeWork:
            self.endTimeHome = self.endTimeWork - 1

    def getLeaveHomeTime():
        convertTime(self.endTimeHome)
     
    def getLeaveWorkTime():
        convertTime(self.endTimeWork)

    def addAction(self, action, location, timeOption, transport):
        self.actions.append({
                "actionType": action,
                "location": location,
                "time": timeOption,
                "legMode": transport
            })
        self.actions.sort(key=lambda action: action["time"]["startTime"])

    def getSchedule(self):
        return self.actions
    
    def __str__(self):
        return "This person lives at " + str(self.house.location) + " and works at " + str(self.work.location) + " which is a(n) " + self.work.type

class House:
    def __init__(self, location):
        self.location = location
        self.transport = None
        self.members = []

    def addMember(self, member):
        self.members.append(member)

    def addTransport(self, transport):
        self.transport = transport

    def __str__(self):
        houseInfo = "This house is located at " + str(self.location) + " and has " + str(len(self.members)) + " members.\n\t"
        houseInfo += "\n\t".join([str(agent) for agent in self.members])
        return houseInfo

class Work:
    def __init__(self, location, workType, area, maxWorkers):
        self.location = location
        self.type = workType
        self.area = area
        self.maxWorkers = maxWorkers
        self.workers = []
        self.hiring = True

    def addWorker(self, worker):
        if self.hiring == False:
            return False
        self.workers.append(worker)
        if len(self.workers) >= self.maxWorkers:
            self.hiring = False
        return True

    def __str__(self):
        return "This job is a(n) " + self.type + " and it is located at " + str(self.location)

def pickTime(timeRange):
    mean = (timeRange[0] + timeRange[1]) / 2
    standardDeviation = timeRange[1] - mean
    timeFloat = random.gauss(mean, standardDeviation)
    return timeFloat

def convertTime(timeFloat):
    hour = int(timeFloat)
    minute = int((timeFloat % 1) * 60)
    timeString = f"{hour:02}:{minute:02}:00"
    return timeString
