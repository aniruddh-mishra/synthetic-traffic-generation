import random
from status import StatusBar
from objects import Person

def genPerson(house, sortedJobs, jobs, sortedLeisureLocations, workFromHomeRatio, workFromHomeTiming):
    workFromHome = random.random() < workFromHomeRatio
    if workFromHome:
        chosenJob = house 
    else:
        while True:
            chosenJob = random.choices(sortedJobs, weights=[len(sortedJobs) - i for i, _ in enumerate(sortedJobs)])[0]
            if not chosenJob.isHiring():
                sortedJobs.remove(chosenJob)
                jobs.remove(chosenJob)
            else:
                break
 

    person = Person(house, chosenJob)
   
    if workFromHome:
        timings = workFromHomeTiming
    else: 
        timingsGuidelines = person.job.timings["work"]["time"]
        timings = timingsGuidelines

        variation = person.job.timings["work"].get("peopleVariation")
        if variation:
            deltaStart = abs(random.gauss(0, variation))
            deltaEnd = abs(random.gauss(0, variation))
            startTime = timingsGuidelines[0] + deltaStart
            startTime = min(max(startTime, timingsGuidelines[0] - variation), timingsGuidelines[0] + variation)
            endTime = timingsGuidelines[1] + deltaEnd
            endTime = min(max(endTime, timingsGuidelines[1] - variation), timingsGuidelines[1] + variation)
            timings = [startTime, endTime]
            if startTime > endTime:
                timings = timingsGuidelines

    # TODO transport
    transport = "car"

    person.addToSchedule("work", person.job, timings, transport)

    sortedLeisureLocations = sortedLeisureLocations.copy()
  
    while True:
        chooseLeisure = random.randint(1, 3) != 1
        if not chooseLeisure:
            break
    
        while True:
            if not len(sortedLeisureLocations):
                return person

            weights = []
            for i, _ in enumerate(sortedLeisureLocations):
                weights.append(len(sortedLeisureLocations) - i)
           
            chosenActivity = random.choices(sortedLeisureLocations, weights=weights)[0]
            activityTimings = chosenActivity.timings["leisure"]["time"].copy()
            if activityTimings[1] < person.getNextAvailable():
                sortedLeisureLocations.remove(chosenActivity)
            else:
                variation = chosenActivity.timings["leisure"].get("peopleVariation")
                activityTimings[0] = max(activityTimings[0], person.getNextAvailable())
                averageDuration = chosenActivity.timings["leisure"].get("averageDuration")
                endTime = activityTimings[0] + averageDuration
                if variation:
                    delta = min(max(0, random.gauss(0, variation)), variation)
                    endTime += delta
                activityTimings[1] = min(activityTimings[1], endTime)
                if activityTimings[1] <= activityTimings[0]:
                    return person
                break
        
        person.addToSchedule("leisure", chosenActivity, activityTimings, transport)
        sortedLeisureLocations.remove(chosenActivity)

    return person

def genHousehold(house, jobs, leisureLocations, cityData, statusBar):
    members = []
    numResidents = house.numResidents
    sortedJobs = sortLocations(house.location, jobs)
    sortedLeisureLocations = sortLocations(house.location, leisureLocations)
    for member in range(numResidents):
        person = genPerson(house, sortedJobs, jobs, sortedLeisureLocations, cityData["workFromHomeRatio"], cityData.get("workFromHomeTiming"))
        if not person.job.isHiring():
            jobs.remove(person.job)
        members.append(person)
        statusBar.updateProgress()
    return members

def sortLocations(reference, listLocations):
    sortFunction = lambda location: pythagoreanTheorem(reference, location.location)
    return sorted(listLocations, key=sortFunction)

def pythagoreanTheorem(pointOne, pointTwo):
    dx = pointOne[0] - pointTwo[0]
    dy = pointOne[1] - pointTwo[1]
    return (dx ** 2 + dy ** 2) ** 0.5

def genHouseholds(locations, cityData):
    homes, jobs, leisureLocations = bucketLocations(locations)
   
    totalPopulation = 0 
    for house in homes:
        totalPopulation += house.numResidents

    people = []
    statusBar = StatusBar(totalPopulation)
    for house in homes:
        people.extend(genHousehold(house, jobs, leisureLocations, cityData, statusBar))

    statusBar.complete()
    
    return people

def bucketLocations(locations):
    homes = []
    jobs = []
    leisureLocations = []
    
    for location in locations:
        if "housing" in location.locationTypes:
            homes.append(location)
        
        if "work" in location.locationTypes:
            jobs.append(location)

        if "leisure" in location.locationTypes:
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
    
    people = genHouseholds(locations, city)

    totalPopulation = 0
    for person in people:
        print(person)
        totalPopulation += 1


    print(f"This city has {totalPopulation} people")

    plt.plot(0, 0)
    plt.legend(loc="upper left")
    plt.show()
