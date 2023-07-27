class Person:
    def __init__(self, house, job):
        self.house = house
        self.job = job
        self.schedule = []

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
        self.schedule.append(task)

    def __str__(self):
        returnString = "Here's some information about this person:\n\n\t* This person has the following schedule: \n"
        counter = 0
        for task in self.schedule:
            counter += 1
            returnString += "\t\t" + str(counter) + ". " + task["actionType"] + " at " + str(task["location"].location) + " from " + str(task["times"][0]) + " to " + str(task["times"][1]) + "\n"
        returnString += "\n\t* This person lives at " + str(self.house.location)
        return returnString + "\n"

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

