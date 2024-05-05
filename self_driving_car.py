import Authentication
import Modules
import Monitor


class Car(Authentication, Modules, Monitor):
    def __init__(self, ):
        # start the monitor session
        Monitor.setup_logging()
        Monitor.send_sys_log("initializing car..", __file__)
    
    def start():
        Monitor.send_sys_log("starting car..", __file__)
        while True:
            print("")