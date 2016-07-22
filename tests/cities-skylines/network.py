from zcm import *

class Network_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        Component.__init__(self)

    def request_update(self):
        """Request the services of a remote server using the client_port"""
        print "Client Timer : Sending message: client_timer_message"
        response = self.client("client_section0").call("client_timer_message")
        print "Client Timer : Received response :", response
