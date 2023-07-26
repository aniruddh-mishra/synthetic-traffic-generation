class Person:
    def __init__(self, house, work):
        self.house = house
        self.work = work

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

class Location:
    def __init__(self, location, locationTypes, numResidents=None, maxWorkers=None):
        self.location = location
        self.locationTypes = locationTypes
        self.numResidents = numResidents
        self.maxWorkers = maxWorkers
        self.timings = None
        self.members = []

    def addMember(self, agent):
        if self.maxMembers and len(self.members) >= self.maxMembers:
            return False
        self.members.append(agent)
        return True

    def __str__(self):
        return f"This node is located at {self.location} and is of the type(s) {', '.join(self.locationTypes)}. It has {self.numResidents} residents and the maximum number of workers here is {self.maxWorkers}"
