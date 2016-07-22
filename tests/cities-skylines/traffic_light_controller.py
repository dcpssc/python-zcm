from zcm import *

class Traffic_light_controller(Component):
    """Register traffic light controller"""
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("updateQ1", self.updateQ1)
        self.register_timer_operation("updateQ2", self.updateQ2)
        self.register_subscriber_operation("getQs", self.getQs)
        self.register_server_operation("next_state", self.next_state)

    def updateQ1(self):
        """publish the length of the queue"""
        q = 1 #
        self.publisher("pub_q").send(str(q))
        print("Queue length", q)

    def updateQ2(self):
        """publish the length of the queue"""
        q = 2 #
        self.publisher("pub_q").send(str(q))
        print("Queue length", q)

    def getQs(self, msg):
        print "Test", msg

    def next_state(self, request):
        """Receive requests for next state"""
        print "Server : Received message", request
        return "ACK"
