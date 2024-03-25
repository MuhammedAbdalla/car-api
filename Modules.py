# EC530 Muhammed Abdalla 2024
# car-api
# API.py

import logging

'''
User Stories:

    API user should be able to add any wheel to the system
    API user should be able to add any LiDAR to the system
    API user should be able to add any obstacle detection system or sensor to the system
    API user should be able to add any camera or visual device to the system
    API user should be able to add any visual object detection to the system
    API user should be able to define starting point and end point of any journey
    API user should be able to interrupt any journey at any time
    API user should be able to get updates on the journey or notifications
    API user should be able to add any path planning module to the system
    API user should be able to get monitoring data anytime requested
    API user should be able to set the speed
    API user should be able to send step by step directions for driving

'''



'''
    module:     Path
    fields:     int[tuple<float,float>] path    [(1.2,0),(-1,45),..(distance,angle)]

    description:
        path is an object containing a array of floating point tuples that contain information about
        how fare forward the car is traveling (in meters) and the turn angle (in degrees)

        0 represents no distance traveled or no turn
        limits are bounded by the wheel turn limit
'''
class Path:
    path = None
    def __init__(self):
        self.path = []
        pass



'''
    module:     Navigation
    fields:     path

    description:
        navigate class takes in Path argument with start and end representing the ID's of the directions in the
        path list. 
        
    methods:    
        __init__()
        navigate()
        
'''
class Navigation(Path):
    path = None
    def __init__(self, path=Path(), start=0,end=0):
        pass

    def navigate():
        pass



'''
    module:     Sensor
    inputs:     string sensor               -> Sensor1

    description:
        sensor class is used to add and define sensors by naming them amd identifying
        their connection port(s) to the car and what comm protocol

    methods:    
            __init__()

'''
class Sensor():
    def __init__(sensor):
        pass


'''
    module:     collision_detection
    fields:     <Object>[] Sensor sensors   -> [Sensor1, Sensor2,... SensorN]
                <float> threshold_redirect  -> x.xxx
    outputs:    <Boolean> detected          -> True/False
                <tuple float>[] position    -> [(dist1, angle1), (dist2, angle2),...(distN, angleN)]
    methods:    
                __init__()
                detect()  


    description:


'''
class CollisionDetection:
    sensors = None
    threshold_redirect = None
    def __init__(self, sensors=list(Sensor), threshold_redirect=0):
        pass

    def detect(self):
        pass


class Wheel():
    wheels = None
    def __init__(self):
        self.wheels = []
        pass
    
    def addWheel(self, name, reverse=False):
        self.wheels.append({"name": name, "speed": 0, "direction": 0, "reverse": False})
        self.updateChassis()
    
    def getWheelProperties(self, wheel):
        for wheel in self.wheels:
            if wheel["name"] == wheel:
                return wheel

    def setWheelProperties(self, wheel, property, val):
        for wheel in self.wheels:
            if wheel["name"] == wheel:
                wheel[property] = val
        self.updateChassis()

    def getSpeed(self, wheel):
        properties = self.getWheelProperties(wheel)
        return properties["speed"]

    def getDirection(self, wheel):
        properties = self.getWheelProperties(wheel)
        return properties["direction"]

    def setSpeed(self, wheel, val):
        # try catch for numerical value, catch -> error log
        self.setWheelProperties(wheel, "speed", val)

    def setDirection(self, wheel, val):
        # try catch for numerical value, catch -> error log
        self.setWheelProperties(wheel, "direction", val)

    def setReverse(self, wheel, val):
        # try catch for boolean value, catch -> error log
        self.setWheelProperties(wheel, "reverse", val)

    def updateChassis(self):
        pass