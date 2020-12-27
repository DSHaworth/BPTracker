import os
import sqlite3
from sqlite3 import Error

class DB_core:

    # create a default path to connect to and create (if necessary) a database
    # called 'database.sqlite3' in the same directory as this script
    dbFileName = "bptracker.sqlite3"

    #https://stackoverflow.com/questions/918154/relative-paths-in-python
    dirname = os.path.dirname(__file__)
    DEFAULT_PATH = os.path.join(dirname, f'../../server/{dbFileName}')

    #DEFAULT_PATH = os.path.join(os.path.dirname(__file__), dbFileName)

    sql_create_table_users = """ 
        CREATE TABLE IF NOT EXISTS users(
            userId INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            dob TEXT NOT NULL,
            image TEXT 
        );"""

    sql_create_table_bpstats = """ 
        CREATE TABLE IF NOT EXISTS bpstats(
            bpStatId INTEGER PRIMARY KEY,
            userId INTEGER NOT NULL,
            sys INTEGER NOT NULL,
            dia INTEGER NOT NULL,
            position TEXT NOT NULL,
            activity TEXT NOT NULL,
            notes TEXT NULL,
            recordDateTime TEXT NOT NULL,
            FOREIGN KEY (userId) REFERENCES users (userId)
        );"""

    sql_create_table_pulse = """ 
        CREATE TABLE IF NOT EXISTS pulse(
            pulseId INTEGER PRIMARY KEY,
            userId INTEGER NOT NULL,
            pulse INTEGER NOT NULL,
            activity TEXT NOT NULL,
            notes TEXT NULL,
            recordDateTime TEXT NOT NULL,
            FOREIGN KEY (userId) REFERENCES users (userId)
        );"""

    sql_create_table_weight = """ 
        CREATE TABLE IF NOT EXISTS weight(
            weightId INTEGER PRIMARY KEY,
            userId INTEGER NOT NULL,
            weight REAL NOT NULL,    
            notes TEXT NULL,
            recordDateTime TEXT NOT NULL,
            FOREIGN KEY (userId) REFERENCES users (userId)
        );"""

    @classmethod
    def create_connection(cls, db_file):
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

    @classmethod
    def create_table(cls, conn, create_table_sql):
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

    @classmethod
    def connect(cls, db_path=DEFAULT_PATH):
        con = cls.create_connection(db_path)

        if con is not None:
            cls.create_table(con, cls.sql_create_table_users)
            cls.create_table(con, cls.sql_create_table_bpstats)
            cls.create_table(con, cls.sql_create_table_pulse)
            cls.create_table(con, cls.sql_create_table_weight)
        else:
            print("Error! cannot create the database connection.")

        return con