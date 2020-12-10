from contextlib import closing
from db_core import DB_core
from models import Weight

class DAL_weight:

    @classmethod
    def add_weight(cls, weight):
        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
                INSERT INTO users 
                    (userId, weight, notes, recordDateTime )
                VALUES
                    (?, ?, ?, ?, ?, ?)""", (weight.userId, weight.weight, weight.notes, weight.recordDateTime,))
            con.commit()
        return weight    
