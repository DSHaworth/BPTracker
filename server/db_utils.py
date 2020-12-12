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

#from models import User
from models import BPStat

from db_core import DB_core
from dal_user import DAL_user

#region BP SQL
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

def main():    
    DAL_user.get_all_users_test()
    #DAL_user.add_user_test()
    #DAL_user.validate_user_test()

if __name__ == "__main__":
    main()
