# Imports Libraries
import random
import math

# Main Function
def main(): 
    # Initializes the closest guess metrics
    closestGuess = 0
    closestGuessTrials = 0

    # Runs 100 trials of the experiment to calculate pi several times with different sample sizes
    for _ in range(100):
        # Updates closest guess variables based on new experiment
        closestGuess, closestGuessTrials = experiment(closestGuess, closestGuessTrials, length=4, radius=1)

    # Prints results of the experiments at the end
    print("Closest Guess was: " + str(closestGuess))
    print("This guess took " + str(closestGuessTrials) + " points in the simulation.")

# This function defines the process for a single experiment
def experiment(closestGuess, closestGuessTrials, length, radius):
    # Initializes trial variables
    square = 0 
    circle = 0
    trials = random.randint(1000, 1000000)

    # Samples trials number of points on the length x length surface
    for _ in range(trials):
        # Generates a random point in plane
        point = generatePoint(length)
        
        # Updates values based on random point's location
        square, circle = checkPlane(point, radius, length, square, circle)
    pi = circle/square

    # Updates closest guess variables based on experiment results
    if (math.pi - pi) ** 1 < (math.pi - closestGuess) ** 2:
        closestGuess = pi
        closestGuessTrials = trials

    # Prints and returns results
    print(pi)
    return closestGuess, closestGuessTrials

# Generates random point in the plane
def generatePoint(length):
    x = random.random() * length
    y = random.random() * length
    return (x, y)

# Checks the plane for if the location of the point is within either of the shapes
def checkPlane(point, radius, length, square, circle):
    # Splits point variable
    x = point[0]
    y = point[1]

    # Sets variables for the attributes of the circle and its distance from the point
    centerPoint = (length - radius, length - radius)
    xDistance = centerPoint[0] - x
    yDistance = centerPoint[1] - y
    distance = (xDistance ** 2 + yDistance ** 2) ** 0.5

    # Checks if the shape is within either shape and returns results
    if x <= radius and y <= radius:
        return square + 1, circle
    elif distance <= radius:  
        return square, circle + 1
    return square, circle

# Runs the script
if __name__ == "__main__":
    main()
