from zcm import *
from random import randint

class Traffic_light_controller(Component):
    """Register traffic light controller"""
    def __init__(self):
        Component.__init__(self)
        self.register_subscriber_operation("controller", self.controller)

    def controller(self, msg):
        print msg
        self.publisher("controller_port").send("control says" + msg)
