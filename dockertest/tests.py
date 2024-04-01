import pytest
import cProfile
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# top level
from Monitor import setup_logging
from Modules import Sensor
from QueueSystem import SensorQueue  # Import the sensor classes

# Set up logging
setup_logging()

# Create a logger
logger = logging.getLogger(__name__)

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
    pr.print_stats()
    pr.dump_stats('prof_data.prof')
    logging.info("end profiling")