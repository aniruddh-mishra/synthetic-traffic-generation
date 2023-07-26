import random
from status import StatusBar
from objects import Person

def genPerson(house, sortedJobs, jobs, sortedLeisureLocations):
    while True:
        chosenJob = random.choices(sortedJobs, weights=[len(sortedJobs) - i for i, _ in enumerate(sortedJobs)])[0]
        if not chosenJob.isHiring():
            sortedJobs.remove(chosenJob)
            jobs.remove(chosenJob)
        else:
            break

    person = Person(house, chosenJob)
    
    timingsGuidelines = person.job.timings["work"]
    timings = timingsGuidelines

    variation = person.job.timings["peopleVariation"].get("work")
    if variation:
        deltaStart = abs(random.gauss(0, variation))
        deltaEnd = abs(random.gauss(0, variation))
        startTime = timingsGuidelines[0] + deltaStart
        endTime = timingsGuidelines[1] + deltaEnd
        timings = [startTime, endTime]

    # TODO transport
    transport = "car"

    person.addToSchedule("work", person.job, timings, transport)

    print(person)
    return person

def genHousehold(house, jobs, leisureLocations):
    members = []
    numResidents = house.numResidents
    sortedJobs = sortLocations(house.location, jobs)
    sortedLeisureLocations = sortLocations(house.location, leisureLocations)
    for member in range(numResidents):
        person = genPerson(house, sortedJobs, jobs, sortedLeisureLocations)
        if not person.job.isHiring():
            jobs.remove(person.job)
        members.append(person)
    return members

def sortLocations(reference, listLocations):
    sortFunction = lambda location: pythagoreanTheorem(reference, location.location)
    return sorted(listLocations, key=sortFunction)

def pythagoreanTheorem(pointOne, pointTwo):
    dx = pointOne[0] - pointTwo[0]
    dy = pointOne[1] - pointTwo[1]
    return (dx ** 2 + dy ** 2) ** 0.5

def genHouseholds(locations):
    homes, jobs, leisureLocations = bucketLocations(locations)
    
    statusBar = StatusBar(len(homes))
    for house in homes:
        genHousehold(house, jobs, leisureLocations)

def bucketLocations(locations):
    homes = []
    jobs = []
    leisureLocations = []
    
    for location in locations:
        if "housing" in location.locationTypes:
            homes.append(location)
        
        if "work" in location.locationTypes:
            jobs.append(location)

        if "leisureLocations" in location.locationTypes:
            leisureLocations.append(location)

    return homes, jobs, leisureLocations

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import json
    from createUniqueZones import genZones
    from createNodes import genAllNodes

    with open('config.json', 'r') as f:
        info = json.load(f)

    zoneInfo = info['zones']
    city = info['city']
    dimensions = city['xLength'], city['yLength']

    cellLength = genZones(dimensions, zoneInfo, info.get('subZones'), plt, random.Random(3))
    print("Generating Nodes...")
    locations = genAllNodes(zoneInfo, cellLength, plt, info.get('subZones'))
    
    genHouseholds(locations)

    plt.plot(0, 0)
    plt.legend(loc="upper left")
    plt.show()

"""
def makeHousehold(node, areaJobs, numPeople, pctWorkFromHome, endTimeRange):
    home = House(node)
    numMembers = random.randint(*numPeople)
    for member in range(numMembers):
        workFromHome = random.random() < pctWorkFromHome
        if workFromHome:
            agent = Person(home, home)
            agent.setLeaveWorkTime(endTimeRange)
        else:
            if len(areaJobs.keys()) == 0:
                continue
            job = findJob(areaJobs)
            if not job:
                print("Add more jobs to config.json, ran out of work")
                return False
            agent = Person(home, job)
            job.addWorker(agent)
            agent.setLeaveHomeTime(job.endTimeRange)

        agent.setLeaveHomeTime(endTimeRange)
        home.addMember(agent)
    
    return home

def findJob(jobs):
    jobs = jobs.copy()
    jobTypes = list(jobs.keys())
    jobType = random.choice(jobTypes)
    jobsInType = jobs[jobType]
    for areaJobs in jobsInType:
        for job in areaJobs:
            if job.hiring:
                return job
    jobs.pop(jobType)
    if len(jobs.keys()) == 0:
        return False
    return findJob(jobs)

def genHouseholds(zones, jobs, pctWorkFromHome):
    households = []
    statusBar = StatusBar(len(zones.keys()))
    for zone, info in zones.items():
        if not info.get('nodes'):
            continue
        if "housing" not in info["types"]:
            continue
        for area, nodes in info["nodes"].items():
            areaJobs = findCloseJobs(area, jobs)
            for node in nodes:
                house = makeHousehold(node, areaJobs, info["numPeople"], pctWorkFromHome, info["endTime"])
                households.append(house)
                if not house:
                    statusBar.fail()
                    return False
        statusBar.updateProgress()

    statusBar.complete()
    return households

def findCloseJobs(area, jobs):
    centralArea = centerOfArea(area)
    jobs = jobs.copy()
    jobs.sort(key=lambda jobArea: pythagoreanTheorem(centerOfArea(jobArea[0].area), centralArea))
    classifiedJobs = {}
    for jobSet in jobs:
        jobType = jobSet[0].type
        if not classifiedJobs.get(jobType):
            classifiedJobs[jobType] = []
        classifiedJobs[jobType].append(jobSet)

    return classifiedJobs

def centerOfArea(area): 
    centerX = (area[2] + area[0]) / 2
    centerY = (area[3] + area[1]) / 2
    return (centerX, centerY)

def pythagoreanTheorem(pointOne, pointTwo):
    dx = pointOne[0] - pointTwo[0]
    dy = pointOne[1] - pointTwo[1]
    return (dx ** 2 + dy ** 2) ** 0.5
"""
