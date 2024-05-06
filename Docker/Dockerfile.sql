# Choose ubuntu version
FROM mcr.microsoft.com/mssql/server:2019-CU13-ubuntu-20.04

# Create app directory
WORKDIR /app

# Copy initialization scripts
COPY . .
             
# Set environment variables, not have to write them with the docker run command
# Note: make sure that your password matches what is in the run-initialization script 
ENV SA_PASSWORD MA1234@stuvi
ENV ACCEPT_EULA Y
ENV MSSQL_PID Express

# Expose port 1433 in case accessing from other container
# Expose port externally from docker-compose.yml
EXPOSE 1433

# Run Microsoft SQL Server and initialization script (at the same time)
CMD /bin/bash ./entrypoint.sh