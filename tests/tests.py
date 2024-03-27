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

def test_format():
    pass

def test_authentication():
    pass

def test_messages():
    pass

def test_monitor():
    pass

def test_modules():
    pass

@pytest.mark.asyncio
async def test_queue():
    sensorQueue = SensorQueue(4, 128)
    # Usage example
    for n in range(32):
        sensor = Sensor(f"SENSOR{n}", f"TEST_SENSOR-{n}", 8080, True)
        sensorQueue.addSensor(sensor)  
    logging.debug("sensors added to queue")

    results = await sensorQueue.processSensors(timeout=3)
    print(results)
    assert 1 == 1


    logging.debug("queued sensors processed")


if __name__ == "__main__":
    logging.info(f"profiling {__name__}")
    pr = cProfile.Profile()
    pr.enable()

    test_queue()

    pr.disable()
    # pr.print_stats()
    pr.dump_stats('prof_data.prof')
    logging.info("end profiling")