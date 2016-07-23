from zcm import *
from random import randint

class Intersection_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        Component.__init__(self)
        #register as subscriber to incoming edges
        self.register_subscriber_operation("updateQueueLength", self.updateQueueLength)
        self.Qs = [randint(0,5) for i in xrange(4)]
        #register timer

    def pub_my_Q(self, msg):
        self.publisher("pushQ").send(msg)

    def keepState(self):
        pass

    def switchState(self):
        pass

    def updateQueueLength(self):
        pass

    def run(self):
        """Timer function to emulate simulation step"""
        if True == self.controllor():
            self.switchState()
            self.clock = 0
        else:
            self.keepState()
            self.clock += 1

class State(object):
    def __init__(self, _state, _phase, _min_interval, _max_interval, _threshold1, _threshold2):
        self.stateRow = _state
        self.phase = _phase
        self.minInterval = _min_interval
        self.maxInterval = _max_interval
        self.threshold1 = _threshold1
        self.threshold2 = _threshold2
