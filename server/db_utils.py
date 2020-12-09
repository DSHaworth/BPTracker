"""
https://stackabuse.com/a-sqlite-tutorial-with-python/

[Create Tables if they don't exit]
https://www.sqlitetutorial.net/sqlite-python/create-tables/

# Testing
> C:/Users/duane/AppData/Local/Programs/Python/Python39/python.exe
>>> from db_utils import db_connect
>>> db_connect()
==================
>>> from db_utils import add_user_test, get_all_users_test, get_user_by_id_test, validate_user_test
>>> add_user_test()

"""
# db_utils.py
import os
import sqlite3
from sqlite3 import Error
from contextlib import closing

from models import User
from models import BPStat

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
dbFileName = "bptracker.sqlite3"
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), dbFileName)

#region User SQL
sql_create_users_table = """ 
    CREATE TABLE IF NOT EXISTS users(
        userId INTEGER PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        dob TEXT NOT NULL,
        image TEXT 
    );"""

sql_insert_user = """
    INSERT INTO users 
        (email, password, firstname, lastname, dob, image)
    VALUES
        (?, ?, ?, ?, ?, ?)"""

sql_update_user = """
    UPDATE users 
        SET 
            email = ?, 
            firstname = ?, 
            lastname = ?, 
            dob = ?, 
            image = ?
        WHERE 
            userId = ?"""

sql_update_user_password = """
    UPDATE users 
        SET 
            password = ?            
        WHERE 
            userId = ?"""

sql_validate_user = """
    SELECT 
        userId, email, password
    FROM
        users
    WHERE
        email=?"""

#endregion

#region BP SQL
sql_create_bpstats_table = """ 
    CREATE TABLE IF NOT EXISTS bpstats(
        bpStatId INTEGER PRIMARY KEY,
        userId INTEGER NOT NULL,
        sys INTEGER NOT NULL,
        dia INTEGER NOT NULL,
        pulse INTEGER NOT NULL,
        bpTaken TEXT NOT NULL,
        position TEXT NOT NULL,
        FOREIGN KEY (userId) REFERENCES users (userId)
    );"""

sql_insert_bpstat = """
    INSERT INTO bpstats
        (userId, sys, dia, pulse, bpTaken, position)
    VALUES
        (?, ?, ?, ?, ?, ?)"""

sql_update_bpstat = """
    UPDATE bpstats
        SET
            sys=?,
            dia=?,
            pulse=?
            bpTaken=?
            position=?
        WHERE
            bpstatId=?"""

sql_get_bpstats_by_userId = """
    SELECT 
        bpStatId, userId, sys, dia, pulse, bpTaken, position
    FROM
        bpstats
    WHERE
        userId=?"""
#endregion

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn

    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def make_user(row):
    return User(userId=row["userId"], email=row["email"], firstname=row["firstname"], lastname=row["lastname"], dob=row["dob"], image=row["image"])

##### TESTS START ############
def add_user_test():
    """
    userId, email, password, firstname, lastname, dob, image
    """
    email=input("email: ")
    password=input("password: ")
    firstname=input("firstname: ")
    lastname=input("lastname: ")
    dob=input("dob: ")

    user = add_user(User(email=email, password=password, firstname=firstname, lastname=lastname, dob=dob))
    print(user)

def get_all_users_test():
    users = get_all_users()
    for user in users:
        print(user.__dict__)

def get_user_by_id_test():
    id = int(input("Id to fetch: "))
    user = get_user_by_id(id)
    if user:
        print(user.__dict__)

def validate_user_test():
    email=input("email: ")
    password=input("password: ")
    user = validate_user(email=email, password=password)

    if user:
        print(user.__dict__)

##### TESTS STOP #############
def add_user(user):
    con = db_connect()
    with closing(con.cursor()) as c:
        c.execute(sql_insert_user, (user.email, user.password, user.firstname, user.lastname, user.dob, user.image,))
        con.commit()
    return user

def get_all_users():
    con = db_connect()
    with closing(con.cursor()) as c:
        c.execute("""
    SELECT 
        userId, email, firstname, lastname, image
    FROM
        users""")
        rows = c.fetchall()

    users = []
    for row in rows:
        users.append(User(userId=row["userId"], email=row["email"], firstname=row["firstname"], lastname=row["lastname"], image=row["image"]))
    return users

def get_user_by_id(id):
    con = db_connect()
    with closing(con.cursor()) as c:
        c.execute("""
    SELECT 
        userId, email, firstname, lastname, image
    FROM
        users
    WHERE
        userId=?""", (id,))
        row = c.fetchone()

    if row:
        return User(userId=row["userId"], email=row["email"], firstname=row["firstname"], lastname=row["lastname"], image=row["image"])
    else:
        return None

def validate_user(email, password):

    con = db_connect()
    with closing(con.cursor()) as c:
        c.execute(sql_validate_user, (email,))
        row = c.fetchone()

    if row:
        if User.authenticate(row["password"], password):
            return get_user_by_id(row["userId"])
        else:
            return None
    else:
        return None

#################################

def authenticate(user):
    pass

def db_connect(db_path=DEFAULT_PATH):
    con = create_connection(db_path)

    if con is not None:
        create_table(con, sql_create_users_table)
        create_table(con, sql_create_bpstats_table)
    else:
        print("Error! cannot create the database connection.")

    return con


def main():    
    get_all_users_test()
    validate_user_test()

if __name__ == "__main__":
    main()
