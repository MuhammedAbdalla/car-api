# requires Sensors module from Module
from Modules import Sensor
from Monitor import *
import logging
import queue
import asyncio

setup_logging()

class SensorQueue():
    sensors = None
    timeout = None

    def __init__(self, maxSize, timeout):
        self.q = queue.Queue(maxsize=maxSize)
        self.timeout = timeout

    def addSensor(self, sensor: Sensor):
        if not isinstance(sensor, Sensor):
            send_sys_err(f"Sensor{sensor.name} must be an instance of SensorBase", "addSensor", logging.WARN)
            raise ValueError(f"Sensor{sensor.name} must be an instance of SensorBase")
        self.q.put(sensor)

    async def sensorData(self, sensor):
        try:
            return await asyncio.wait_for(sensor.getData(), self.timeout)
        except asyncio.TimeoutError:
            send_sys_err(f"Timeout: Failed to retrieve data from {sensor.name}", "addSensor", logging.WARN)
            return f"Timeout: Failed to retrieve data from {sensor.name}"
    
    async def processQueue(self):
        results = []
        while not self.q.empty():
            sensor = self.q.get()
            result = await self.sensorData(sensor)
            results.append((sensor, result))
            # store results in sensors table in DB
            self.q.task_done()
            
        return results

