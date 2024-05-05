import pyodbc
import Monitor
import logging
import hashlib

def __hash_function__(username, password):
    combined_string = username + password
    sha512 = hashlib.sha512()
    sha512.update(combined_string.encode())
    password_hash = sha512.hexdigest()[:128]

    return password_hash


def authorize():
    pass

    
def login(conn, username, password, reg=False):
    print("logging in")
    # print(username, password)
    # check for spaces and check for 1 OR 1
    password_hash = __hash_function__(username, password)
    if reg:
        return register(conn, username, password_hash)
    else:
        try:
            cursor = conn.cursor()
            query = f''' 
                SELECT username, password_hash FROM Car.Users
                WHERE username = ? AND password_hash = ?
            '''
            cursor.execute(query, (username, password_hash))
            row = findCursorData(cursor, username)
            
            if row == None:
                return False, None
            if username in row and password_hash in row:
                return True, None
        except pyodbc.Error as e:
            Monitor.send_sys_err(f"SQL Server Error: {e}", login.__name__, logging.ERROR)
            return False, e

    return False, None


def register(conn, username, password_hash):
    print("registering")
    try:
        cursor = conn.cursor()
        query = f''' 
            SELECT username FROM Car.Users
            WHERE username = ? AND password_hash = ?
        '''
        cursor.execute(query, (username, password_hash))

        # failure registration: duplicates
        if len(cursor.fetchall()) > 0:
            Monitor.send_sys_err("SQL DB: Car.Users: duplicates users found", register.__name__, logging.WARN)
            return False, None
        
        # successful registration
        query = f'''
            INSERT INTO Car.Users (username, password_hash, permission)
            VALUES (?, ?, ?)
        '''
        cursor.execute(query, (username, password_hash, 0b001))
        conn.commit()
        return True, None
    
    except pyodbc.Error as e:
        Monitor.send_sys_err(f"SQL Server Error: {e}", register.__name__, logging.ERROR)
        return False, e
    

def removeUser(conn, username, password):
    Monitor.send_sys_log(f"removing user: {username}", removeUser.__name__)
    try:
        password_hash = __hash_function__(username, password)
        cursor = conn.cursor()
        query = "DELETE FROM Car.Users WHERE username = ? AND password_hash = ?"
        cursor.execute(query, (username, password_hash))
        conn.commit()
    except pyodbc.Error as e:
        Monitor.send_sys_err(f"SQL Server Error: {e}", removeUser.__name__, logging.ERROR)
        return False, e

    return True, None


def fetchData(conn, query, args):
    try:
        cursor = conn.cursor()
        # Query the database
        cursor.execute(query, args)
        readCursor(cursor)
    except pyodbc.Error as e:
        Monitor.send_sys_err(f"SQL Server Error: {e}", fetchData.__name__, logging.ERROR)
        return False, e
    
    return True, None


def readCursor(cursor):
    for row in cursor:
        print(row)

def findCursorData(cursor, data):
    for row in cursor:
        if data in row:
            return row
    return None

'''
    examples:

    # Update data
    cursor.execute("UPDATE Employees SET Salary = 85000 WHERE Id = 1")

    # Delete data
    cursor.execute("DELETE FROM Employees WHERE Id = 1")

    conn.commit()

'''


def connectDB(server, uid, pwd, trusted):
    Monitor.send_sys_msg(f"connecting to {server} uid:{uid} pwd:{pwd}")
    conn = None
    try:
        # Create the connection string
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE=CAR_API;'
            f'UID={uid};'
            f'PWD={pwd};'
            f'Trusted_Connection={trusted};'
        )
    except pyodbc.Error as e:
        Monitor.send_sys_err(f"SQL Server Error: {e}", connectDB.__name__, logging.CRITICAL)
        # Additional error handling or cleanup:
        return False, e
    
    return True, conn

