import random
from objects import Work
from status import StatusBar

def genJobsInZone(nodes, workType, area, numWorkers):
    jobs = []
    for node in nodes:
        job = Work(node, workType, area, numWorkers)
        jobs.append(job)
    return jobs

def genJobs(zones):
    allJobs = []
    for zone, info in zones.items():
        if not info.get('nodes') or "work" not in info["types"]:
            continue
        
        print(len(info["nodes"].keys()), "area in working zone", zone)
        statusBar = StatusBar(len(info["nodes"].keys()))
        for area, nodes in info["nodes"].items():
            allJobs.append(genJobsInZone(nodes, zone, area, info["numWorkers"]))
            statusBar.updateProgress()
        statusBar.complete()

    return allJobs
