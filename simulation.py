import numpy as np
import simpy


class passengerGenerator:
    def __init__(self, env, stop):
        self.stop = stop
        self.action = env.process(self.run())

    def run(self):
        while True:
            wait = np.random.exponential(1/self.stop.getParameter())
            bin.put(1)
            yield env.timeout(wait)


class busStop:
    def __init__(self, env, label, parameter):
        self.bin = simpy.Container(env)
        self.label = label
        self.parameter = parameter

    def getParameter(self):
        return self.parameter
    
    def getBinLevel(self):
        return self.bin.level

    def pickUp(self, n):
        return self.bin.get(n)


class routeSelector:
    def __init__(self, env, routes):
        self.routes = routes
        self.action = env.process(self.run())

    def pickRoute(self):
        routeKeys = list(self.routes.keys())
        index = np.random.randint(len(routeKeys))
        return self.routes[routeKeys[index]]

    def run(self):
        while True:
            yield self.


class bus:
    def __init__(self, env, capacity, route):
        self.capacity = capacity
        self.passengerCount = 0
        self.setRoute(route)
        self.action = env.process(self.run())
        
    def pickUp(self, n):
        self.routeStops[self.currentProgress].pickUp(n)

    def setRoute(self, route):
        self.routeStops = route[1]
        self.routeRoads = route[2]
        self.routeLength = len(self.routeRoads)
        self.currentProgress = 0

    def advance(self):
        self.currentProgress += 1

    def run(self):
        while True:
            if self.currentProgress + 1 == self.routeLength:
                self.setRoute()
            yield env.timeout(self.routeRoads[self.currentProgress])
            # calculate pickup n
            # pickup
            # advance


if __name__ == "__main__":
    env = simpy.Environment()

    # stops
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
    stopList = [s1e, s1w,
                s2e, s2w,
                s3e, s3w,
                s4e, s4w,
                s5e, s5w,
                s6e, s6w,
                s7e, s7w]

    # road travel times
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

    # generator
    for stop is stopList:
        generator = passengerGenerator(env, stop)

    # route name: [[stops], [roads]]
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
    env.process(passengerGenerator(env))
    env.process(bus(env))
    env.run()
