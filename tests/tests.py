# top level
import pytest
import cProfile
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Monitor import setup_logging
from Authentication import *
from Modules import *
from QueueSystem import SensorQueue  # Import the sensor classes

# Set up logging
setup_logging()

# Create a logger
logger = logging.getLogger(__name__)

def test_format():
    pass

def test_authentication():
    logging.debug("TESTING AUTHENTICATION MODULE")
    # Define your connection parameters
    server = 'MUHABDALLA\\SQLEXPRESS'  # The double backslashes are necessary in Python strings
    database = 'CAR_API'  # Replace with your database name
    isConn, conn = connectDB(server, database)
    assert isConn == True # CHECKPOINT 1; EST DB CONN

    isQuery, _ = fetchData(conn, "SELECT * FROM Car.Users", ())
    assert isQuery == True
    
    isPass, _ = login(conn, "muhammed", "abc123", True)
    assert isPass == True

    isPass, _ = login(conn, "adfsdas", "abc123", True)
    assert isPass == True

    isPass, _ = removeUser(conn, "muhammed", "abc123")
    assert isPass == True

    isQuery, _ = fetchData(conn, "SELECT * FROM Car.Users", ())
    assert isQuery == True

    isQuery, _ = fetchData(conn, "SELECT id, username FROM Car.Users WHERE username = ?", ("muhammed",))
    assert isQuery == True
    
    conn.close()

def test_messages():
    pass

def test_monitor():
    pass

def test_modules():
    pass

def test_db():
    pass

@pytest.mark.asyncio
async def test_queue():
    sensorQueue = SensorQueue(128, 0.75)
    logging.debug(f"Creating Sensor Queue | max size : 128 | timeout : {sensorQueue.timeout}")
    # Usage example
    for n in range(32):
        sensor = Sensor(f"TEST_SENSOR[{n}]", f"T.XXX", 8080, testMode=True)
        sensorQueue.addSensor(sensor)  
    logging.debug(f"added 32 sensors to queue")

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