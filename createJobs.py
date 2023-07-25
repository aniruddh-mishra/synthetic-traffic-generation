import random
from objects import Work

def genJobsInZone(nodes, workType, area, numWorkers):
    jobs = []
    for node in nodes:
        job = Work(node, workType, area, numWorkers)
        jobs.append(job)
    return jobs

def genJobs(zones):
    allJobs = []
    for zone, info in zones.items():
        if not info.get('nodes'):
            continue
        if info["type"] != "work" and info["type"] != "leisure":
            continue
        
        for area, nodes in info["nodes"].items():
            allJobs.append(genJobsInZone(nodes, zone, area, info["numWorkers"]))

    return allJobs
