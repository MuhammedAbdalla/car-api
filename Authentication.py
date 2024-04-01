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
    try:
        cursor = conn.cursor()
        query = f''' 
            SELECT username, password_hash FROM Car.Users
            WHERE username = ? AND password_hash = ?
        '''
        cursor.execute(query, (username, password_hash))
    except pyodbc.Error as e:
        print(f"SQL Server Error: {e}")
        return False, e

    if reg:
        register(conn, username, password_hash)
    
    # readCursor(cursor)

    return True, None


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
            logging.warning("SQL DB: Car.Users: duplicates users found")
            print("duplicate users found")
            return False
        
        # successful registration
        query = f'''
            INSERT INTO Car.Users (username, password_hash, permission)
            VALUES (?, ?, ?)
        '''
        cursor.execute(query, (username, password_hash, 0b001))
        conn.commit()
    except pyodbc.Error as e:
        print(f"SQL Server Error: {e}")
        return False, e
    
    return True, None


def removeUser(conn, username, password):
    print("removing user:", username)
    try:
        password_hash = __hash_function__(username, password)
        cursor = conn.cursor()
        query = "DELETE FROM Car.Users WHERE username = ? AND password_hash = ?"
        cursor.execute(query, (username, password_hash))
        conn.commit()
    except pyodbc.Error as e:
        print(f"SQL Server Error: {e}")
        return False, e

    return True, None

def fetchData(conn, query, args):
    try:
        cursor = conn.cursor()
        # Query the database
        cursor.execute(query, args)
        readCursor(cursor)
    except pyodbc.Error as e:
        print(f"SQL Server Error: {e}")
        return False, e
    
    return True, None


def readCursor(cursor):
    for row in cursor:
        print(row)

'''
    examples:

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
        fetchData(conn, "SELECT * FROM Car.Users", ())
        # user = input("enter your username: ")
        # password = input("enter your password: ")
        # login(conn, "muhammed", "abc123", True)
        # login(conn, "adfsdas", "abc123", True)
        # removeUser(conn, "muhammed", "abc123")
        # fetchData(conn, "SELECT * FROM Car.Users", ())
        # fetchData(conn, "SELECT id, username FROM Car.Users WHERE username = ?", ("muhammed",))

    except pyodbc.Error as e:
        print(f"SQL Server Error: {e}")
        # Additional error handling or cleanup:
        conn.close()