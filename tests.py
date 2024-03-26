from Modules import Sensor
from QueueSystem import SensorQueue  # Import the sensor classes
import cProfile
import logging
import asyncio

def test_format():
    pass

def test_queue():
    async def func():
        queue = SensorQueue()
        # Usage example
        for n in range(32):
            sensor = Sensor(f"SENSOR{n}", f"TEST_SENSOR-{n}", 8080, True)
            queue.addSensor(sensor)  
        logging.info("sensors added to queue")

        results = await queue.processSensors(timeout=3)
        print(results)
        logging.info("queued sensors processed")
    
    asyncio.run(func())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        filename='app.log', 
        filemode='a', 
        format='%(asctime)s [%(process)d %(name)s] %(levelname)s: %(message)s'
    )
    logging.info(f"profiling {__name__}")
    pr = cProfile.Profile()
    pr.enable()

    test_queue()

    pr.disable()
    # pr.print_stats()
    pr.dump_stats('prof_data.prof')
    logging.info("end profiling")