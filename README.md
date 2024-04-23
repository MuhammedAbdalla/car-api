# EC530 Car API with Self-Driving modules
## Project 2 & Final Project

```
API user should be able to add any wheel to the system
API user should be able to add any LiDAR to the system
API user should be able to add any obstacle detection system or sensor to the system
API user should be able to add any camera or visual device to the system
API user should be able to add any visual object detection to the system
API user should be able to define starting point and end point of any journey
API user should be able to interrupt any journey at any time
API user should be able to get updates on the journey or notifications
API user should be able to add any path planning module to the system
API user should be able to get monitoring data anytime requested
API user should be able to set the speed
API user should be able to send step by step directions for driving
```
# the code

**app.py** the main python file to host the API <br>
**Authentication.py** register or login to the car API with user & password <br>
[WIP] **Messages.py** messages class to construct and setup info, warning & error messages <br>
**Modules.py** python class file containing: Navigation, Sensor, Detection and Chassis classes for the Car API <br>
[WIP] **Monitor.py** set up logging and messaging in the Car API using logging and a central file <br>
**QueueSystem.py** python implementation of a queue in software with asynchronous functions to account for sensor lag/delay <br>
<hr>

# testing

### dev testing
**pytest.ini** defines the parameters in which to log all levels from DEBUG into logs/pytest.log <br> 
[WIP] tests for every module + app.py <br>
pytest
```
pytest tests/tests.py
```
coverage testing over pytest
```
coverage run -m pytest tests/tests.py
```
### docker testing
Only tests in docker is for QueueSystem.py along with the associated modules <br>
[WIP] tests for every module + app.py
```
cd dockertest
docker run dockerfile
```
