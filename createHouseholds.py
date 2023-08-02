from status import StatusBar
from objects import Person

def genPerson(house, sortedJobs, jobs, sortedLeisureLocations, cityData, random):
    randomSelector = random.random()
    workFromHome = randomSelector < cityData["workFromHomeRatio"]
    workFromZone = not workFromHome and randomSelector < cityData["workFromZoneRatio"]
    if workFromHome:
        chosenJob = house 
    else:
        while True:
            if not len(sortedJobs):
                chosenJob = house
                workFromHome = True
                print("Ran out of jobs, adding extra work from home person.")
                break
            chosenJob = random.choices(sortedJobs, weights=[len(sortedJobs) - i for i, _ in enumerate(sortedJobs)])[0]
            if not chosenJob.isHiring() or (not workFromZone and chosenJob.zone == house.zone):
                sortedJobs.remove(chosenJob)
                jobs.remove(chosenJob)
            else:
                break
 
    person = Person(house, chosenJob)
    chosenJob.addWorker(person)
    person.workFromHome = workFromHome

    if workFromHome:
        timings = cityData.get("workFromHomeTiming")
    else: 
        timingsGuidelines = person.job.timings["work"]["time"]
        timings = timingsGuidelines

        variation = person.job.timings["work"].get("peopleVariation")
        if variation:
            deltaStart = abs(random.gauss(0, variation))
            deltaEnd = abs(random.gauss(0, variation))
            startTime = timingsGuidelines[0] + deltaStart
            startTime = min(max(startTime, timingsGuidelines[0]), timingsGuidelines[0] + variation)
            endTime = timingsGuidelines[1] + deltaEnd
            endTime = min(max(endTime, timingsGuidelines[1] - variation), timingsGuidelines[1])
            timings = [startTime, endTime]
            if startTime > endTime:
                timings = timingsGuidelines

    transport = "bicycle"
    if house.hasCar(timings):
        transport = "car"
        house.checkoutCar(timings)
    person.currentVehicle = transport

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
       
        if transport != "car" and house.hasCar(activityTimings):
            transport = "car"
            person.addToSchedule("home", house, [activityTimings[0], activityTimings[0]], transport)

        if transport == "car" and not house.hasCar(activityTimings):
            transport = "bicycle"
            person.addToSchedule("home", house, [activityTimings[0], activityTimings[0]], transport)

        if transport == "car":
            house.checkoutCar(activityTimings)

        person.addToSchedule("leisure", chosenActivity, activityTimings, transport)
        sortedLeisureLocations.remove(chosenActivity)

    return person

def genHousehold(house, jobs, leisureLocations, cityData, statusBar, random):
    homesWithCarsRatio = cityData["homesWithCarsRatio"]
    hasCar = random.random() < homesWithCarsRatio
    if hasCar:
        transport = []
        numCars = random.randint(*cityData["numCarsInHome"])
        for car in range(numCars):
            transport.append({
                "times": []
            })
        house.transport = transport

    members = []
    sortedJobs = sortLocations(house.location, jobs, sortJobsFunction)
    sortedLeisureLocations = sortLocations(house.location, leisureLocations, sortLeisureFunction)

    for _ in range(house.houseEquivalence):
        numResidents = house.numResidents
        for member in range(numResidents):
            person = genPerson(house, sortedJobs, jobs, sortedLeisureLocations, cityData, random)
            if not person.job.isHiring() and not person.workFromHome:
                jobs.remove(person.job)
                sortedJobs.remove(person.job)
            members.append(person)
            statusBar.updateProgress()
    return members

def sortLocations(reference, listLocations, function):
    sortFunction = lambda location: function(reference, location)
    return sorted(listLocations, key=sortFunction)

def sortLeisureFunction(reference, location):
    return pythagoreanTheorem(reference, location.location)

def sortJobsFunction(reference, location):
    score = pythagoreanTheorem(reference, location.location)
    if location.maxWorkers:
        return score / location.maxWorkers
    return score

def pythagoreanTheorem(pointOne, pointTwo):
    dx = pointOne[0] - pointTwo[0]
    dy = pointOne[1] - pointTwo[1]
    return (dx ** 2 + dy ** 2) ** 0.5

def genHouseholds(locations, cityData, random):
    homes, jobs, leisureLocations = bucketLocations(locations)
   
    totalPopulation = 0 
    for house in homes:
        totalPopulation += house.numResidents

    people = []
    print(f"Total Population: {totalPopulation}")
    statusBar = StatusBar(totalPopulation)
    for house in homes:
        people.extend(genHousehold(house, jobs, leisureLocations, cityData, statusBar, random))

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
    from createZones import genZones
    from createNodes import genAllNodes
    import random

    with open('config.json', 'r') as f:
        info = json.load(f)

    zoneInfo = info['zones']
    city = info['city']
    dimensions = city['xLength'], city['yLength']

    cellLength, _ = genZones(dimensions, zoneInfo, info.get('subZones'), plt, random.Random(1))
    print("Generating Nodes...")
    locations, regions = genAllNodes(zoneInfo, cellLength, plt, info.get('subZones'), random.Random(1))

    print("Generating Households")
    people = genHouseholds(locations, city, random.Random(1))

    totalPopulation = 0
    for person in people:
        print(person)
        totalPopulation += 1


    print(f"This city has {totalPopulation} people")

    plt.plot(0, 0)
    plt.legend(loc="upper left")
    plt.show()
