from zcm import *
from random import randint

class Network_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("sim_step", self.sim_step)
        self.q = randint(0,5)
        print "q is:" , self.q

    def updateQueueLength(self, q):
        self.publisher("pub_light1").send(str(q))
        print "network sent queue"

    def sim_step(self):
        self.q = self.q + randint(0, 2)
        self.updateQueueLength(self.q)
