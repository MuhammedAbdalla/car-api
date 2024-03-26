# requires Sensors module from Module
from Modules import Sensor
import queue
import asyncio

class SensorQueue:
    sensors = None

    def __init__(self):
        self.q = queue.Queue(maxsize=128)

    def addSensor(self, sensor: Sensor):
        if not isinstance(sensor, Sensor):
            raise ValueError("Sensor must be an instance of SensorBase")
        self.q.put(sensor)


    async def sensorData(self, sensor, timeout):
        try:
            return await asyncio.wait_for(sensor.getData(), timeout)
        except asyncio.TimeoutError:
            return f"Timeout: Failed to retrieve data from {type(sensor).__name__}"

    async def processSensors(self, timeout=10):
        results = []
        while not self.q.empty():
            sensor = self.q.get()
            result = await self.sensorData(sensor=sensor, timeout=timeout)
            results.append(result)
            self.q.task_done()
        return results




