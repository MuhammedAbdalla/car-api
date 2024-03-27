# requires Sensors module from Module
from Modules import Sensor
from Monitor import setup_logging
import logging
import threading
import queue
import asyncio

setup_logging()

class SensorQueue:
    sensors = None
    threads = None
    numThreads = None

    def __init__(self, numThreads, maxSize):
        self.q = queue.Queue(maxsize=maxSize)
        self.numThreads = numThreads
        self.threads = []

    def addSensor(self, sensor: Sensor):
        if not isinstance(sensor, Sensor):
            logging.warning(f"Sensor{sensor.name} must be an instance of SensorBase")
            raise ValueError(f"Sensor{sensor.name} must be an instance of SensorBase")
        self.q.put(sensor)

    def distributeData(self):
        counter = 0
        threadArgs = [[] for _ in range(self.numThreads)]
        while not self.q.empty():
            sensor = self.q.get()
            threadArgs[counter%self.numThreads].append(sensor)
            threadArgs[counter%self.numThreads]
            logging.info(f"added sensor{sensor.name} to thread{counter%self.numThreads}")
            counter += 1
            self.q.task_done()
        
        for i in range(self.numThreads):
            t = threading.Thread(name=f"thread_{i}",target=self.processSensors, args=(threadArgs[i],0.5,), daemon=True)
            self.threads.append(t)


    async def sensorData(self, sensor, timeout):
        try:
            return await asyncio.wait_for(sensor.getData(), timeout)
        except asyncio.TimeoutError:
            logging.warning(f"Timeout: Failed to retrieve data from {type(sensor).__name__}")
            return f"Timeout: Failed to retrieve data from {type(sensor).__name__}"

    async def processSensors(self, data, timeout):
        results = []
        for sensor in data:
            result = await self.sensorData(sensor=sensor, timeout=timeout)
            results.append(result)
            # store results in sensors table in DB
        return results


