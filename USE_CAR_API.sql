USE CAR_API

INSERT INTO Car.Users (username, password_hash, permission)
VALUES ('test', '12345678\0', '101')

SELECT TOP (20) [id]
      ,[username]
      ,[password_hash]
      ,[permission]
  FROM [CAR_API].[Car].[Users]