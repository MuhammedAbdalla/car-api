import Authentication
import Modules
import Monitor


class Car:
    def __init__(self):
        # start the monitor session
        Monitor.setup_logging()
        Monitor.send_sys_log("initializing car..", __file__)
    
    def start():
        Monitor.send_sys_log("starting car..", __file__)
        while True:
            print("")


        # # add 6 collision detection sensors
        # for i in range(6):
        #     cdSensor = Sensor(f"cdSensor-{i+1}", "collision",5000+i,True) # set test mode to true for now
        #     cdSystem.addSensor(cdSensor)