import pyodbc
import random
import Monitor
import logging
import hashlib

def __hash_function__(username, password):
    combined_string = username + password
    sha512 = hashlib.sha512()
    sha512.update(combined_string.encode())
    password_hash = sha512.hexdigest()[:128]

    return password_hash

def Authorize(conn, username, password):
    # print(user, password)
    # check for spaces and check for 1 OR 1
    password_hash = __hash_function__(username, password)
    try:
        cursor = conn.cursor()
        cursor.execute(f''' 
            SELECT username, password_hash FROM Car.Users
            WHERE username IS {username} AND password_hash IS {password_hash}
        ''')
        readCursor(cursor)
        return True
    except pyodbc.Error as e:
        print(f"SQL Server Error: {e}")

    register(conn, username, password_hash)
    return False
    


def login(conn, username, password_hash):

    return True


def register(conn, username, password_hash):
    cursor = conn.cursor()
    query = f'''
        INSERT INTO Car.Users (username, password_hash, permission)
        VALUES (?, ?, ?)
    '''
    cursor.execute(query, (username, password_hash, 0b001))
    conn.commit()


def removeUser(conn, username):
    cursor = conn.cursor()
    query = "DELETE FROM Car.Users WHERE username = ?"
    cursor.execute(query, (username,))
    conn.commit()


def fetchUsers(conn):
    cursor = conn.cursor()
    # Query the database
    cursor.execute("SELECT * FROM Car.Users")
    readCursor(cursor)


def readCursor(cursor):
    for row in cursor:
        print(row)

'''
    # Update data
    cursor.execute("UPDATE Employees SET Salary = 85000 WHERE Id = 1")

    # Delete data
    cursor.execute("DELETE FROM Employees WHERE Id = 1")

    conn.commit()

'''
if __name__ == "__main__":
    Monitor.setup_logging()
    logging.debug("TESTING AUTHENTICATION MODULE")
    # Define your connection parameters
    server = 'MUHABDALLA\\SQLEXPRESS'  # The double backslashes are necessary in Python strings
    database = 'CAR_API'  # Replace with your database name
    conn = None
    try:
        # Create the connection string
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        # user = input("enter your username: ")
        # password = input("enter your password: ")
        Authorize(conn, "muhammed", "abc123")
        fetchUsers(conn)

    except pyodbc.Error as e:
        print(f"SQL Server Error: {e}")
        # Additional error handling or cleanup:
        conn.close()