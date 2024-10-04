import numpy as np
import simpy
import matplotlib.pyplot as plt


class passengerGenerator:
    def __init__(self, env, stop):
        self.stop = stop
        self.action = env.process(self.run())
        self.env = env

    def run(self):
        while True:
            self.stop.addPassenger(passenger(self.env, self.stop))
            wait = np.random.exponential(1/self.stop.getParameter())
            yield env.timeout(wait)


class busStop:
    def __init__(self, env, label, parameter):
        # self.bin = simpy.Container(env)
        self.bin = simpy.Store(env)
        self.label = label
        self.parameter = parameter

    def getParameter(self):
        return self.parameter
    
    def getPassengerCount(self):
        # return self.bin.level
        return len(self.bin.items)

    def pickUp(self, bus, n):
        if self.parameter == None:
            return 0
        # return self.bin.get(n) # TODO kan man ta ut n?
        for i in range(n):
            # passenger = self.bin.get()
            passenger = yield self.bin.get()
            passenger.embark(bus)
    
    def addPassenger(self, passenger):
        self.bin.put(passenger)
        
    def toString(self):
        return self.label


class routeSelector:
    def __init__(self, env, routes):
        self.routes = routes
        #self.action = env.process(self.run())
    
    def calculateWeight(self, route):
        passengerCount = 0
        for stop in route: 
            passengerCount += stop.getPassengerCount()
        return passengerCount

    def pickRoute(self, startStop):
        weight = 0
        bestRoute = None
        for key in self.routes.keys():
            currentRoute = self.routes[key]
            if currentRoute[1][0] == startStop:
                currentWeight = self.calculateWeight(currentRoute[1])
                if currentWeight >= weight:
                    weight = currentWeight
                    bestRoute = currentRoute
        return bestRoute


class passenger:
    def __init__(self, env, stop):
        self.spawnTime = env.now
        self.stop = stop

    def leaveBus(self):
        pass
        # TODO log travel time

    def embark(self, bus):
        bus.addPassenger(self)


class bus:
    def __init__(self, env, capacity, routeSelector, busID, startStop):
        self.capacity = capacity
        self.passengerCount = 0
        self.routeSelector = routeSelector
        self.setRoute(startStop)
        self.busID = busID
        self.utilizationLog = []
        self.action = env.process(self.run())
        
    def pickUp(self, n):
        self.getCurrentStop().pickUp(self, n)
        self.passengerCount += n
    
    def dropOff(self):
        self.passengerCount -= 1

    def setRoute(self, startStop=None):
        if startStop:
            route = self.routeSelector.pickRoute(startStop)
        else:
            route = self.routeSelector.pickRoute(self.routeStops[-1])
        
        self.currentProgress = 0
        self.passengerCount = 0
        self.routeStops = route[1]
        self.routeRoads = route[2]
        self.routeLength = len(self.routeRoads)
    
    def getCurrentStop(self):
        return self.routeStops[self.currentProgress+1]
    
    def getUtilizationLog(self):
        return self.utilizationLog
    
    def calculatePickUpCount(self):
        waitingPassengers = self.getCurrentStop().getPassengerCount()
        maxPickup = self.capacity - self.passengerCount
        if(waitingPassengers < maxPickup):
            return waitingPassengers
        return maxPickup
        
    def run(self):
        while True:
            if self.currentProgress >= self.routeLength:
                self.setRoute()
            else:    
                # Collect utilization statistcs
                self.utilizationLog.append(self.passengerCount * self.routeRoads[self.currentProgress] / self.capacity)
                
                # Drop off passengers
                for passenger in range(self.passengerCount):
                    if np.random.rand() < Q:
                        self.dropOff()

                # Pick up passengers
                pickUpCount = self.calculatePickUpCount()
                if pickUpCount > 0:
                    self.pickUp(pickUpCount)
                print(f"Bus {self.busID} has {self.passengerCount} passengers at {self.getCurrentStop().toString()}, at time {env.now}")
                

                yield env.timeout(self.routeRoads[self.currentProgress])
                self.currentProgress += 1


def setupAndRun(env, simTime, n_b):
    # Stops
    e1 = busStop(env, "e1", None)
    e2 = busStop(env, "e2", None)
    s1e = busStop(env, "s1e", 0.3)
    s1w = busStop(env, "s1w", 0.6)
    s2e = busStop(env, "s2e", 0.1)
    s2w = busStop(env, "s2w", 0.1)
    s3e = busStop(env, "s3e", 0.3)
    s3w = busStop(env, "s3w", 0.9)
    s4e = busStop(env, "s4e", 0.2)
    s4w = busStop(env, "s4w", 0.5)
    s5e = busStop(env, "s5e", 0.6)
    s5w = busStop(env, "s5w", 0.4)
    s6e = busStop(env, "s6e", 0.6)
    s6w = busStop(env, "s6w", 0.4)
    s7e = busStop(env, "s7e", 0.5)
    s7w = busStop(env, "s7w", 0.4)
    e3 = busStop(env, "e3", None)
    e4 = busStop(env, "e4", None)
    endStops = [e1, e2, e3, e4]
    stopList = [s1e, s1w,
                s2e, s2w,
                s3e, s3w,
                s4e, s4w,
                s5e, s5w,
                s6e, s6w,
                s7e, s7w]

    # Road travel times
    r1 = 3
    r2 = 7
    r3 = 6
    r4 = 1
    r5 = 4
    r6 = 3
    r7 = 9
    r8 = 1
    r9 = 3
    r10 = 8
    r11 = 8
    r12 = 5
    r13 = 6
    r14 = 2
    r15 = 3

    # Passenger generators
    for stop in stopList:
        passengerGenerator(env, stop)
    
    # Routes
    routes = {
            "E1E3": ["e", [e1, s1e, s4e, s6e, e3], [r1, r5, r8, r13]],
            "E1E4": ["e", [e1, s2e, s5e, s7e, e4], [r2, r7, r11, r15]],
            "E2E3": ["e", [e2, s2e, s5e, s6e, e3], [r3, r7, r9, r13]],
            "E2E4": ["e", [e2, s3e, s7e, e4], [r4, r12, r15]],
            "E3E1": ["w", [e3, s6w, s4w, s1w, e1], [r13, r8, r5, r1]],
            "E4E1": ["w", [e4, s7w, s5w, s2w, e1], [r15, r11, r7, r2]],
            "E3E2": ["w", [e3, s6w, s5w, s2w, e2], [r13, r9, r7, r3]],
            "E4E2": ["w", [e4, s7w, s3w, e2], [r15, r12, r4]]
            }
    
    # Create multiple buses
    selector = routeSelector(env, routes)
    busList = []
    for i in range(n_b):
        startStop = endStops[np.random.randint(len(endStops))] # Randomly pick a start position
        busObject = bus(env, 20, selector, i+1, startStop)
        busList.append(busObject)
    
    # Run simulation
    env.run(until=simTime)
    
    # Calculate utilization
    averageUtilList = []
    for busInstance in busList:
        util_list = np.array(busInstance.getUtilizationLog())
        averageUtil = sum(util_list)/simTime
        averageUtilList.append(averageUtil)
    return np.mean(np.array(averageUtilList))


if __name__ == "__main__":
    global Q 
    Q = 0.3 # Passenger leave probability
    simTime = 600
    n_b = [5, 7, 10, 15]
    
    # Run simulation multiple times
    SE_list = []
    outerAverageUtilizationList = []
    for value in n_b:
        averageUtilizationList = []
        for i in range(15):
            env = simpy.Environment()
            averageUtilization = setupAndRun(env, simTime, value)
            averageUtilizationList.append(averageUtilization)
        outerAverageUtilizationList.append(np.mean(np.array(averageUtilizationList)))
        SDsum = 0
        for observation in averageUtilizationList:
            #SD += np.observation - (np.mean(np.array(averageUtilizationList))/len(averageUtilizationList)-1)
            #SE = SD/np.sqrt(len(averageUtilizationList))
            #SE_list.append(SE)
            SDsum += (observation-np.mean(np.array(averageUtilizationList)))**2
        SD = np.sqrt(SDsum/(len(averageUtilizationList)-1))
        SE_list.append(SD/np.sqrt(len(averageUtilizationList)))
                
    # Print average utilization
    for i in range(len(n_b)):
        print(f"{n_b[i]} buses results in an average utilization of {100*outerAverageUtilizationList[i]:.2f}% with standard error {SE_list[i]}.")
    
    plt.figure(figsize=(8, 6))
    x_pos = np.arange(len(outerAverageUtilizationList))
    plt.bar(x_pos, outerAverageUtilizationList, yerr=SE_list, align='center', alpha=0.7, capsize=10, color='skyblue')
    plt.xticks(x_pos, n_b)
    plt.ylabel('Average utilization')
    plt.grid()
    plt.show()
