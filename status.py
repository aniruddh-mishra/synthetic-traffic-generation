import time
import sys

class StatusBar:
    def __init__(self, totalNum, width=10, characterComplete="=", characterInComplete="-"):
        self.totalNum = totalNum
        self.width = width
        self.characterComplete = characterComplete
        self.characterInComplete = characterInComplete
        self.progress = 0
        self.lastShown = None
        self.averageTime = None
        self.ETA = None
        self.startTime = time.perf_counter()

    def setETA(self):
        now = time.perf_counter()
        duration = now - self.startTime
        self.averageTime = duration / self.progress
        numLeft = self.totalNum - self.progress
        self.ETA = self.averageTime * numLeft

    def updateProgress(self, progress=1):
        self.progress += progress
        self.setETA()
        now = time.perf_counter()
        if self.lastShown and now - self.lastShown < 1 and self.progress != self.totalNum:
            return 
        self.lastShown = now
        self.printStatus()
    
    def complete(self):
        if self.progress == self.totalNum:
            return
        self.progress = self.totalNum
        if self.progress == 0:
            return
        self.setETA()
        self.printStatus()

    def fail(self):
        self.progress = 0
        self.ETA = None
        self.printStatus()
        print("Failed!")

    def printStatus(self):
        pct = self.progress / self.totalNum
        numCompleteBars = int(self.width * pct)
        numIncomplete = self.width - numCompleteBars
        stringPrint = '[' + self.characterComplete * numCompleteBars + self.characterInComplete * numIncomplete + ']' + str(round(pct * 100, 2)) + "% "
        if self.ETA != None:
            stringPrint += "ETA: " + str(round(self.ETA)) + " seconds"

        print(stringPrint)

        if self.ETA and self.progress != self.totalNum: 
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

if __name__ == "__main__":
    bar = StatusBar(10, 10)
    for i in range(10):
        time.sleep(2)
        bar.updateProgress()
    bar.complete()

