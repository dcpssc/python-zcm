from zcm import *
from random import randint
import config
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json
from time import time
import socket

class Intersection_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        print("initialize")
        Component.__init__(self)
        #queue parameters?
        self.Qs = [randint(0,2) for i in xrange(4)] #[N E S W]
        self.minInterval = [5, 5]
        self.maxInterval = [10, 20]
        self.threshold1 = [30, 30] #if density % is lower don't switch
        self.threshold2 = [70, 70] #if density % if higher don't switch
        self.statesList = ['1', '2']
        #self.stateMask = ['0202']
        self.currentIdx = 0
        self.clock = 0
        #pp.pprint(self.clock)
        #register timer
        self.register_timer_operation("update", self.update)
        #register subscriber function
        self.register_subscriber_operation("coordinateN", self.coordinateN)
        self.register_subscriber_operation("coordinateE", self.coordinateE)
        self.register_subscriber_operation("coordinateS", self.coordinateS)
        self.register_subscriber_operation("coordinateW", self.coordinateW)
        #self.sensors = ['N', 'E', 'S', 'W']
        #pp.pprint(self.name) name hasn't been set yet...?
        #how do you call a function immediately after running __init__?
        self.initialized = False
        self.sock = socket.socket(socket.SOCK_DGRAM)
        #self.sock.bind((UDP_IP, UDP_PORT))

    def update(self):
        #print self.clock
        #print self.Qs
        #print self.statesList[self.currentIdx]
        if not self.initialized:
            self.initialized = True
            self.State = self.getState()
            self.clock = time()

        if True == self.controllor():
            self.switchState()
            self.clock = time()
        else:
            self.keepState()
            #self.clock += 1
        #self.simStep(self.statesList[self.currentIdx])

        #NEED SOME WAY TO FIGURE OUT WHO NEIGHBORS ARE
        NQmsg = [self.name, "NQ", self.Qs[0], self.statesList[self.currentIdx]]
        self.publisher("pushNQ").send(str(NQmsg))
        #self.publisher("pushEQ").send(self.name + str(self.Qs[1]))
        #self.publisher("pushSQ").send(self.name + str(self.Qs[2]))
        #self.publisher("pushWQ").send(self.name + str(self.Qs[3]))
        #print "pushed"
        #print self.name

    def controllor(self):
        currentState = self.statesList[self.currentIdx]
        if (time() - self.clock) < self.minInterval[self.currentIdx]:
            return False

        if (time() - self.clock) >= self.maxInterval[self.currentIdx]:
            return True

        #get queue data
        redQ = 0
        GreenQ = 0

        for idx, i in enumerate(self.State):
            if (self.State[i]['vehicle']) == 'Green':
                self.Qs[idx] = self.getDensity(i)
                GreenQ += self.Qs[idx]
            elif (self.State[i]['vehicle']) == 'Red':
                self.Qs[idx] = self.getDensity(i)
                redQ += self.Qs[idx]
            else:
                assert False

        # for i in xrange(len(currentState)):
        #     if '2' == currentState[i]:
        #         redQ += self.Qs[i]
        #     elif '0' == currentState[i]:
        #         GreenQ += self.Qs[i]
        #     else:
        #         assert False

        if redQ <= self.threshold1[self.currentIdx]:
            print "redQ", redQ
            return False

        if GreenQ > self.threshold2[self.currentIdx]:
            print "GreenQ", GreenQ
            return False
        else: #q1 > threshold1 and q2 < threshold2
            #print "true"
            return True

    def switchState(self):
        self.currentIdx = (self.currentIdx + 1) % len(self.statesList)
        for i in self.State:
            if (self.State[i]['vehicle']) == 'Green':
                self.setState(i, "Red", "Red")
            elif (self.State[i]['vehicle']) == 'Red':
                self.setState(i, "Green", "Red")
            else:
                assert False

    def keepState(self):
        pass

    # def simStep(self, currentState):
    #     for i in xrange(len(currentState)):
    #         if '2' == currentState[i]:
    #             self.Qs[i] += randint(0, 1)
    #         elif '0' == currentState[i]:
    #             self.Qs[i] += randint(-self.Qs[i], 1)
    #         else:
    #             assert False

    def coordinate(self, msg, segment):
        #(name, state, queue )
        #(compare states)
        pp.pprint(str(self.name) + segment + " segment received " + msg)

    def coordinateN(self, msg):
        self.coordinate(msg, "N")
    def coordinateE(self, msg):
        self.coordinate(msg, "E")
    def coordinateS(self, msg):
        self.coordinate(msg, "S")
    def coordinateW(self, msg):
        self.coordinate(msg, "W")

        #print str(self.name) + " N segment received " + msg
        #pp.pprint(self.__dict__)
        #pp.pprint("message" + msg)

    def getState(self):
        """
            else if (request.Method == MethodType.GETSTATE)
            {
                object nodeIdObj = GetObject(request.Object);
                int nodeId = Convert.ToInt32(nodeIdObj);
                retObj = GetNodeState(nodeId);
            }
        """
        data = {
                'Method': 'GETSTATE',
                'Object': {
                	       'Name': 'NodeId',
                           'Type': 'PARAMETER',
                           'Value': self.name,  #// should be 0 - 3 (for the selected ids)
                           'ValueType': 'System.UInt32'
                           }
               }
        data_string = json.dumps(data)

        #response = self.send(data_string)
        #state = json.load(response)
        with open('dummy.json') as node_string:
            state = json.load(node_string)
        #pp.pprint(state)
        return state

    def getDensity(self, segment):
        data = {
                'Method': 'GETDENSITY',
                'Object':{
                            'Name': 'NodeId',
                        	'Type': 'PARAMETER',
                        	'Value': int(self.name),  #// should be 0 - 3 (for the selected ids)
                        	'ValueType': 'System.UInt32',
                        	'Parameters':
                            [
                        	    {
                        		'Name': 'SegmentId',
                        		'Type': 'PARAMETER',
                        		'Value': segment,
                        		'ValueType': 'System.UInt32'
                        	    }
                            ]
                         }
                }
        data_string = json.dumps(data)

        #response = self.send(data_string)
        #density = json.load(response)
        density = randint(0, 100)
        return density

    def setState(self, segment, vehicleState, pedestrianState ):
        data = {
                'Method': 'SETSTATE',
                'Object':
                            {
                            'Name': 'NodeId',
                            'Type': 'PARAMETER',
                            'Value': int(self.name),  #// should be 0 - 3 (for the selected ids)
                            'ValueType': 'System.UInt32',
                            'Parameters':
                                        [
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': segment,
                                            'ValueType': 'System.UInt32'	    },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': vehicleState,
                                            'ValueType': 'System.String'	    },
                                    	    {
                                    		'Name': 'PedestrianState',
                                    		'Type': 'PARAMETER',
                                    		'Value': 'Red',
                                    		'ValueType': 'System.String'
                                    	    }
	                                    ]
                            }
                }
        data_string = json.dumps(data)

        #response = self.send(data_string)
        response = "ACK"
        return response

    def send(self, data_string):
        self.sock.settimeout(1)
        self.sock.sendto(data_string, ("191.168.127.100",11000))

        try:
            response, srvr = self.sock.recvfrom(1024)
        except timeout:
            response = ""
            print 'Request timed out'
        return response
