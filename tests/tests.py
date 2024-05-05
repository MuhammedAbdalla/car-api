# top level
import pytest
import cProfile
import logging
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Monitor import setup_logging
from Authentication import *
from Modules import *
from QueueSystem import SensorQueue  # Import the sensor classes

import self_driving_car

# Set up logging
setup_logging()

# Create a logger
logger = logging.getLogger(__name__)

def test_navigation():
    logging.debug("TESTING NAVIGATION MODULE\n\tBEGIN")
    nav = Navigation()

    # travel in a sin wave
    paths = [Path(0,0)]
    start = 1
    step = 5
    itr = 1000
    for x in range(start,itr,step):
        d_x = step
        d_y = math.sin(x) - math.sin(x-1)
        distance = math.sqrt(d_y**2 + d_x**2)
        direction = math.atan2(d_y/d_x)
        
        paths.append(Path(distance,direction))


def test_authentication():
    logging.debug("TESTING AUTHENTICATION MODULE\n\tBEGIN")
    server = None 
    uid = None
    pwd = None
    if os.getenv('DOCKER_CONTAINER') == 'true':
        logging.debug("Running in a Docker container")
        server = 'sql_server_db' 
        uid = 'sa'
        pwd = 'U45097807@Stuvi'
    else:
        logging.debug("Not running in a Docker container")
        server = 'localhost\\SQLEXPRESS' 
        uid = 'sa'
        pwd = 'MA1234@stuvi'


    # Get testing environment
    # Define your connection parameters
    # server = 'localhost'  # The double backslashes are necessary in Python strings
    # database = 'CAR_API'  # Replace with your database name
    isConn, conn = connectDB(server, uid, pwd)
    assert isConn == True # CHECKPOINT 1; EST DB CONN
    logging.debug(" SQL: DB connection - passed")

    isQuery, _ = fetchData(conn, "SELECT * FROM Car.Users", ())
    assert isQuery == True
    logging.debug(" SQL: Select Query - passed")
    
    isPass, _ = login(conn, "muhammed", "abc123", False)
    assert isPass == True
    logging.debug(" SQL: Good Login - passed")

    isPass, _ = login(conn, "DOESNT_EXIST", "abc123", False)
    assert isPass == False
    logging.debug(" SQL: Bad Login - passed")

    isPass, _ = removeUser(conn, "muhammed", "abc123")
    assert isPass == True
    logging.debug(" SQL: Remove User - passed")

    isQuery, _ = fetchData(conn, "SELECT id, username FROM Car.Users WHERE username = ?", ("muhammed",))
    assert isQuery == True
    logging.debug("TESTING AUTHENTICATION MODULE\n\tEND")
    
    conn.close()
    logging.debug(" SQL: Register - passed")
    
def test_monitor():
    pass

def test_chassis():
    logging.debug("TESTING CHASSIS")

    chassis = Chassis()
    chassis.tankMode = False # normal driving
    chassis.createWheelGroup("rear", [Wheel("back left"), Wheel("back right")])
    chassis.createWheelGroup("left-steer", [Wheel("front left")])
    chassis.createWheelGroup("right-steer", [Wheel("front right")])

    logging.debug(" Forward drive")
    # go forward

    for name, wheelGroup in chassis.wheelGroups.items():
        for wheel in wheelGroup:
            wheel.setSpeed(5)
            wheel.direction = 0

    # go backwards
    for name, wheelGroup in chassis.wheelGroups.items():
        for wheel in wheelGroup:
            wheel.setSpeed(-5)
            wheel.direction = 0

    # go right
    for wheel in chassis.wheelGroup["left-steer"]:
        wheel.setSpeed(5)
        wheel.direction = -45

    for wheel in chassis.wheelGroup["right-steer"]:
        wheel.setSpeed(5)
        wheel.direction = -45

    for wheel in chassis.wheelGroup["rear"]:
        wheel.setSpeed(5)
        wheel.direction = 0

    # go left
    for wheel in chassis.wheelGroup["left-steer"]:
        wheel.setSpeed(5)
        wheel.direction = 45

    for wheel in chassis.wheelGroup["right-steer"]:
        wheel.setSpeed(5)
        wheel.direction = 45

    for wheel in chassis.wheelGroup["rear"]:
        wheel.setSpeed(5)
        wheel.direction = 0

def test_car():
    pass

@pytest.mark.asyncio
async def test_queue():
    sensorQueue = SensorQueue(128, 0.75)
    logging.debug(f"Creating Sensor Queue | max size : 128 | timeout : {sensorQueue.timeout}")
    # Usage example
    for n in range(10):
        sensor = Sensor(f"TEST_SENSOR[{n}]", f"T.XXX", 8080, testMode=True)
        sensorQueue.addSensor(sensor)  
    logging.debug(f"added 10 sensors to queue")

    results = await sensorQueue.processQueue()
    logging.debug("results:")
    for sensor, result in results:  
        logging.debug(f"\t{sensor.name} : {result}")
    

    logging.debug("queued sensors processed")
    assert 1==1


if __name__ == "__main__":
    logging.info(f"profiling {__name__}")
    pr = cProfile.Profile()
    pr.enable()

    test_queue()

    pr.disable()
    # pr.print_stats()
    pr.dump_stats('prof_data.prof')
    logging.info("end profiling")