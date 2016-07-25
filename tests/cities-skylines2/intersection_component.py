from zcm import *
from random import randint
import numpy as np
import config

class Intersection_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        print("initialize")
        Component.__init__(self)
        #register as subscriber to incoming edges
        #self.register_subscriber_operation("updateQueueLength", self.updateQueueLength)
        #queue parameters?
        self.Qs = [randint(0,2) for i in xrange(4)]
        #register timer
        self.statesList = ['1010', '0101']
        self.currentIdx = 0
        #self.sensors = ['N', 'E', 'S', 'W']
        self.clock = 0
        self.register_timer_operation("update", self.update)
        self.register_subscriber_operation("coordinate", self.coordinate)
        self.minInterval = [0, 0]
        self.maxInterval = [10, 20]
        self.threshold1 = [3,3]
        self.threshold2 = [4,4]

    def update(self):
        #print self.clock
        #print self.Qs
        #print self.statesList[self.currentIdx]
        if True == self.controllor():
            self.switchState()
            self.clock = 0
        else:
            self.keepState()
            self.clock += 1
        self.simStep(self.statesList[self.currentIdx])

        self.publisher("pushQN").send(str(self.Qs[0]))
        self.publisher("pushQE").send(str(self.Qs[1]))
        self.publisher("pushQS").send(str(self.Qs[2]))
        self.publisher("pushQW").send(str(self.Qs[3]))
        print "pushed"

    def controllor(self):
        currentState = self.statesList[self.currentIdx]
        if self.clock < self.minInterval[self.currentIdx]:
            return False

        if self.clock >= self.maxInterval[self.currentIdx]:
            return True

        #get queue data
        redQ = 0
        GreenQ = 0
        for i in xrange(len(currentState)):
            if '0' == currentState[i]:
                redQ += self.Qs[i]
            elif '1' == currentState[i]:
                GreenQ += self.Qs[i]
            else:
                assert False

        if redQ <= self.threshold1[self.currentIdx]:
            #print "redQ", redQ
            return False

        if GreenQ > self.threshold2[self.currentIdx]:
            #print "GreenQ", GreenQ
            return False
        else: #q1 > threshold1 and q2 < threshold2
            #print "true"
            return True

    def switchState(self):
        self.currentIdx = (self.currentIdx + 1) % len(self.statesList)

    def keepState(self):
        pass

    def simStep(self, currentState):
        for i in xrange(len(currentState)):
            if '0' == currentState[i]:
                self.Qs[i] += randint(0, 1)
            elif '1' == currentState[i]:
                self.Qs[i] += randint(-self.Qs[i], 1)
            else:
                assert False

    def coordinate(self, msg):
        print msg
