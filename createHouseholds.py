import random
from objects import Person, House

def makeHousehold(node, areaJobs, numPeople):
    home = House(node)
    numMembers = random.randint(*numPeople)
    for member in range(numMembers):
        if len(areaJobs.keys()) == 0:
            continue
        job = findJob(areaJobs)
        if not job:
            print("Add more jobs to config.json, ran out of work")
            return False
        agent = Person(home, job)
        job.addWorker(agent)
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

def genHouseholds(zones, jobs):
    households = []
    for zone, info in zones.items():
        if not info.get('nodes'):
            continue
        if info["type"] != "housing":
            continue
        for area, nodes in info["nodes"].items():
            areaJobs = findCloseJobs(area, jobs)
            for node in nodes:
                house = makeHousehold(node, areaJobs, info["numPeople"])
                households.append(house)
                if not house:
                    return False
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

