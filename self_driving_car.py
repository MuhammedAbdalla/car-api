import Authentication
import Monitor
from QueueSystem import *
from Modules import *


class Car():
    def __init__(self):
        # start the monitor session
        Monitor.setup_logging()
        Monitor.send_sys_log("initializing car..", __file__)
    
    def start(self):
        Monitor.send_sys_log("initializing database connection..", __file__)
        server = 'localhost\\sqlexpress' #input("enter instance >> ")
        uid = 'sa' #input("enter username >> ")
        passwd = 'MA1234@stuvi' #input("enter password >> ")
        Authentication.connectDB(server, uid, passwd, "yes")

        Monitor.send_sys_log("starting car..", __file__)

        file = 'tests/car.sdc' #input("enter your car '\.sdc'\ file >> ")
        with open(file, 'r') as car_file:
            chassis = Chassis()
            sensors = SensorQueue(32, 5)
            cdSys = CollisionDetection(5)
        
            for line in car_file.readlines():
                line_tok = line.split(":")
                if len(line_tok) > 1:
                    components = line_tok[1].split(',')
                    if line_tok[0] == "wheel":
                        chassis.addToWheelGroup(components[1], Wheel(components[0]))
                    if line_tok[0] == "sensor":
                        if components[1] == "CollisionDetection":
                            cdSys.addSensor(Sensor(components[0],components[1],components[2], True))
                        else:
                            sensors.addSensor(Sensor(components[0],components[1],components[2], True))

if __name__ == "__main__":
    car = Car()
    car.start()