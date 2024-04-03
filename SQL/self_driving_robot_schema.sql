
-- Muhammed Abdalla & Ahmet
-- Authentication and Authorization Module
-- 64 bit size username
-- MD5 Hash 128 bits

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'CAR_API')
BEGIN
    CREATE DATABASE CAR_API;
END
GO

USE CAR_API;
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Sensors')
BEGIN
    EXEC('CREATE SCHEMA Sensors');
    PRINT 'Sensors Schema created successfully';
END
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Car')
BEGIN
    EXEC('CREATE SCHEMA Car');
    PRINT 'Car Schema created successfully';
END

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Logs')
BEGIN
    EXEC('CREATE SCHEMA Logs');
    PRINT 'Logs Schema created successfully';
End

-- SENSORS
-- LiDAR Module
CREATE TABLE Sensors.LiDAR (
    id INT PRIMARY KEY IDENTITY,
    time_stamp DATETIME2 DEFAULT CURRENT_TIMESTAMP,
    distance_readings FLOAT  
);

-- Camera Module
CREATE TABLE Sensors.Camera (
    id INT PRIMARY KEY IDENTITY,
    time_stamp DATETIME2 DEFAULT CURRENT_TIMESTAMP,
    image_data VARBINARY (MAX),
);

-- CAR
CREATE TABLE Car.Users (
    id INT PRIMARY KEY IDENTITY,
    username VARCHAR (64) NOT NULL,
    password_hash char (128) NOT NULL,
    permission INT NOT NULL DEFAULT 0
);

-- Visual Object Detection Module
CREATE TABLE Car.DetectedObjects (
    id INT PRIMARY KEY IDENTITY,
    camera_feed_id INT,
    time_stamp DATETIME2 DEFAULT CURRENT_TIMESTAMP,
    object_type TEXT,
    confidence FLOAT,
    position FLOAT, 
    FOREIGN KEY(camera_feed_id) REFERENCES Sensors.Camera(id)
);

-- Navigation Module
CREATE TABLE Car.NavigationRoutes (
    id INTEGER PRIMARY KEY IDENTITY,
    start_point FLOAT,
    end_point FLOAT,
    created_at DATETIME2 DEFAULT CURRENT_TIMESTAMP
);

-- Collision Avoidance Detection
CREATE TABLE Car.CollisionDetection (
    id INT PRIMARY KEY IDENTITY,
    time_stamp DATETIME2 DEFAULT CURRENT_TIMESTAMP,
    severity INT,
    information TEXT
);

-- LOGS
CREATE TABLE Logs.AccessLogs (
    id INT PRIMARY KEY IDENTITY,
    user_id INTEGER,
    time_stamp DATETIME2 DEFAULT CURRENT_TIMESTAMP,
    command TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES Car.Users(id)
);

-- Wheel Module
CREATE TABLE Logs.WheelCommands (
    id INTEGER PRIMARY KEY IDENTITY,
    time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    speed FLOAT,
    direction VARCHAR (64),
    direction_angle FLOAT,
    duration INT
);

-- Monitoring
CREATE TABLE Logs.SystemHealth (
    id INT PRIMARY KEY IDENTITY,
    time_stamp DATETIME2 DEFAULT CURRENT_TIMESTAMP,
    component CHAR (64),
    component_status CHAR (64),
    component_information CHAR (64)
);