class Person:
    def __init__(self, house, job):
        self.house = house
        self.job = job
        self.schedule = []

    def getNextAvailable(self):
        scheduleTasks = list(self.schedule.values())
        return scheduleTasks[-1][1]

    def addToSchedule(self, actionType, location, times, transport):
        task = {
            "actionType": actionType,
            "location": location,
            "times": times,
            "transportTo": transport
        }
        self.schedule.append(task)

    def addAction(self, action, location, timeOption, transport):
        self.actions.append({
                "actionType": action,
                "location": location,
                "time": timeOption,
                "legMode": transport
            })
        self.actions.sort(key=lambda action: action["time"]["startTime"])

    def __str__(self):
        return f"This person has the following schedule: {self.schedule}" 

class Location:
    def __init__(self, location, locationTypes, numResidents=None, maxWorkers=None):
        self.location = location
        self.locationTypes = locationTypes
        self.numResidents = numResidents
        self.maxWorkers = maxWorkers
        self.timings = None
        self.workers = []

    def addMember(self, agent):
        if self.maxWorkers and len(self.workers) >= self.maxWorkers:
            return False
        self.workers.append(agent)
        return True

    def isHiring(self):
        return not self.maxWorkers or len(self.workers) < self.maxWorkers

    def __str__(self):
        return f"This node is located at {self.location} and is of the type(s) {', '.join(self.locationTypes)}. It has {self.numResidents} residents and the maximum number of workers here is {self.maxWorkers}. The timings for this location are set to {self.timings}"

