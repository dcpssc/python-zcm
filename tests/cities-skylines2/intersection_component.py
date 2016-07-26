from zcm import *
from random import randint
import numpy as np
import config
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json

class Intersection_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        print("initialize")
        Component.__init__(self)
        #queue parameters?
        self.Qs = [randint(0,2) for i in xrange(4)] #[N E S W]
        #self.State = self.getState()
        self.minInterval = [0, 0]
        self.maxInterval = [10, 20]
        self.threshold1 = [10, 10] #if density % is lower don't switch
        self.threshold2 = [70, 70] #if density % if higher don't switch
        self.statesList = ['2020', '0202']
        self.currentIdx = 0
        self.clock = 0
        #register timer
        self.register_timer_operation("update", self.update)
        #register subscriber function
        self.register_subscriber_operation("coordinate", self.coordinate)

        #self.sensors = ['N', 'E', 'S', 'W']

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

        NQmsg = [self.name, "NQ", self.Qs[0], self.statesList[self.currentIdx]]
        self.publisher("pushNQ").send(str(NQmsg))
        #self.publisher("pushEQ").send(self.name + str(self.Qs[1]))
        #self.publisher("pushSQ").send(self.name + str(self.Qs[2]))
        #self.publisher("pushWQ").send(self.name + str(self.Qs[3]))
        #print "pushed"
        #print self.name

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
            elif '2' == currentState[i]:
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
        #(name, state, queue )
        #(compare states)
        print str(self.name) + " received " + msg
        pp.pprint(self.__dict__)

    def getState():
        data = {
                'Method': 'GETSTATE',
                'Object': {
                	       'Name': 'NodeId',
                           'Type': 'PARAMETER',
                           'Value': int(self.name),  #// should be 0 - 3 (for the selected ids)
                           'ValueType': 'System.UInt32'
                           }
               }
        data_string = json.dumps(data)
        #state = self.client("Network_Port").call(data_string)
        state = [2, 0, 2, 0]
        return state

    def getDensity(segment):
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
        #density = self.client("Network_Port").call(data_string)
        density = 20
        return density

    def setState:
        data = {
                'Method': 'SETSTATE',
                'Object':
                            {
                            'Name': 'NodeId',
                            'Type': 'PARAMETER',
                            'Value': 0,  #// should be 0 - 3 (for the selected ids)
                            'ValueType': 'System.UInt32',
                            'Parameters':
                                        [
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': 0,
                                            'ValueType': 'System.UInt32'	    },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': "Red",
                                            'ValueType': 'System.String'	    },
                                    	    {
                                    		'Name': 'PedestrianState',
                                    		'Type': 'PARAMETER',
                                    		'Value': "Red",
                                    		'ValueType': 'System.String'
                                    	    }
	                                    ]
                            }
                }
        data_string = json.dumps(data)
        #response = self.client("Network_Port").call(data_string)
        response = "ACK"
        return response
