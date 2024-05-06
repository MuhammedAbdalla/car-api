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
### self_driving_car.py
the main python file to host the API <br>

### Authentication.py 
register or login to the car API with user & password <br>

### Monitor.py 
Monitor class to construct and setup info, warning & error messages <br>
Also abstracts from logging class to provide user messages, errors and failures in the API <br>

### Modules.py 
python class file containing: Navigation, Sensor, Detection and Chassis classes for the Car API <br>

### QueueSystem.py
python implementation of a queue in software with asynchronous functions to account for sensor lag/delay <br>

currently this API is hosted on the local machine due to the nature of embedded system projects. HTTP frameworks to host car controls is a  future implementation <br>
To run car API, you need microsoft SQL server on your machine so the database schema executes into a new database called CAR_API <br>

![image](https://github.com/MuhammedAbdalla/car-api/assets/54071115/39074898-3f60-4e0e-9c31-7a25c34bfa4c)

```
python self_driving_car.py
```
### definitions
A car can be abstrated into sub-components such as wheel, sensors, navigation, monitor, etc. The implementation of this project provide laxed modularity for the car. Car are defined in '.sdc' files (self driving car extension) and are formatted such as <br>
```
component: name, type, misc 1, misc 2, misc 3....
```
![image](https://github.com/MuhammedAbdalla/car-api/assets/54071115/2d688bc3-8078-4b58-9ad4-f692b8e20c07)

<hr>

# testing

## dev testing
**pytest.ini** defines the parameters in which to log all levels from DEBUG into logs/pytest.log <br> 
tests for every module + app.py <br>
using pytest

![image](https://github.com/MuhammedAbdalla/car-api/assets/54071115/5644afd7-0460-4ea0-86cc-f586d87804df)

```
pytest tests/tests.py
```
coverage testing over pytest
```
coverage run -m pytest tests/tests.py
```
### [WIP] docker testing

API has test cases specifically for Monitor, Navigation, Wheels and Sensors <br>

![image](https://github.com/MuhammedAbdalla/car-api/assets/54071115/70fd050b-51a0-4024-a98c-8bd584ca0bb9)

Authentication for Docker is not responding due to permission errors with sql container and mssql settings <br>
To deploy the API: <br>
```
>> cd Docker
>> bash
$ ./deploy.sh
$ docker-compose up
```

![image](https://github.com/MuhammedAbdalla/car-api/assets/54071115/397a8b03-d1c8-4711-9285-2c2c420cb0ca)


