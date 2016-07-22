from zcm import *
from random import randint

class Network_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("sim_step", self.sim_step)
        self.register_subscriber_operation("switchState", self.switchState)
        self.networkQ = [randint(0,5) for i in xrange(10)]
        print self.networkQ

    def updateQueueLength(self, q):
        self.publisher("pub_light").send("light_0 " + str(q))
        print "network sent queue"

    def sim_step(self):
        self.networkQ[1] += randint(0, 2)
        self.updateQueueLength(self.networkQ[1])

    def switchState(self, msg):
        print "switch to ", msg

# this represents cities skyline simulation.
# it publishes the current queues
# it subscribes to
