# EC530 Muhammed Abdalla 2024
# car-api
# API.py

import random
import asyncio
import Monitor
import threading

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
    def __init__(self, distance, direction):
        self.path = (distance, direction)



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
class Navigation:
    def __init__(self, threshold_redirect):
        self.paths = []
        self.distanceTraveled = 0
        self.orientation = 0
        self.threshold_redirect = threshold_redirect
    
    def addPath(self, path: Path):
        if isinstance(path, Path):
            self.paths.append(path)

    def stepPath(self):
        return self.paths.pop(0)

    def execute(self):
        Monitor.send_sys_msg(f"enabling collision detection")
        cdSystem = CollisionDetection(self.threshold_redirect)
        cdSystem.start()
        self.enabled = True

        def start():
            Monitor.send_sys_msg(f"executing navigation\n# paths: {len(self.paths)}")
            while self.paths and self.enabled:
                distance, direction = self.stepPath().path

                self.distanceTraveled += distance
                self.orientation += direction % 360
                Monitor.send_sys_msg(f" path: {distance}, {direction}\n \
                                        total distance: {self.distanceTraveled} \
                                        car orientation: {self.orientation} \
                                ")
        threading.Thread(target=start(), args=(), daemon=True).start()
    
    def stop(self):
        self.enabled = False
             

'''
    module:     Sensor
    inputs:     string sensor               -> Sensor1

    description:
        sensor class is used to add and define sensors by naming them amd identifying
        their connection port(s) to the car and what comm protocol

    methods:    
            __init__()
            

'''
class Sensor:
    sensorName = None
    sensorType = None
    sensorPort = None
    testMode = False

    def __init__(self, sensorName, sensorType, sensorPort, testMode):
            self.name = sensorName
            self.sensorType = sensorType
            self.sensorPort = sensorPort
            self.testMode = testMode
        
    async def getData(self):
        if self.testMode:
            await asyncio.sleep(random.random())
            return random.random()*100
        else:
            # pyserial to use serial communication for sensors
            # this would also use asyncio methods to retrieve data
            pass
        return None


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
    def __init__(self, threshold_redirect):
        self.sensors = []
        self.threshold_redirect = threshold_redirect
    
    def addSensor(self, sensor: Sensor):
        if isinstance(sensor, Sensor):
            self.sensors.append(sensor)


    def start(self):
        async def detect(sensor, threshold_redirect):
            while True:
                result = await sensor.getData()
                if result <= threshold_redirect:
                    Monitor.send_sys_msg(f" obstacle detected: {result} units ahead")
                    

        for sensor in self.sensors:
            threading.Thread(target=detect, args=(sensor,self.threshold_redirect), daemon=True).start()


class Wheel:
    name = None
    speed = None
    direction = None
    reverse = None

    def __init__(self, name, reverse=False):
        self.name = name
        self.speed = 0
        self.direction = 0
        self.reverse = reverse

    def getSpeed(self):
        return self.speed

    def getDirection(self):
        return self.direction
            
    def setSpeed(self, val):
        # try catch for numerical value, catch -> error log
        if self.reverse:
            self.speed = -val
        else:
            self.speed = val

    def setDirection(self, val):
        # try catch for numerical value, catch -> error log
        self.direction = val

    def setReverse(self, val):
        # try catch for boolean value, catch -> error log
        self.reverse = val


class Chassis:
    wheels = None
    wheelGroups = None
    tankMode = False

    def __init__(self):
        self.wheels = []
        self.wheelGroups = {}
        pass
    
    def addWheel(self, nameWheel):
        wheel = Wheel(name=nameWheel)
        self.wheels.append(wheel)
        self.updateChassis()

    def removeWheel(self, name):
        idx = self.wheels.index(self.getWheel(name))
        if idx > -1:
            self.wheels.pop(idx)
        self.updateChassis()

    def getWheel(self, wheel):
        for wheel in self.wheels:
            if wheel.name == wheel:
                return wheel
    
    def createWheelGroup(self, wheelGroupID, wheels):
        self.wheels.extend(wheels)
        self.wheelGroups[wheelGroupID] = wheels
        self.updateChassis()
    
    def setAttribute(self, wheelGroupID, attr, val):
        for wheel in self.wheelGroups[wheelGroupID]:
            if attr == "speed":
                wheel.setSpeed(val)
            elif attr == "direction":
                wheel.setDirection(val)

    def updateChassis(self):
        pass
        