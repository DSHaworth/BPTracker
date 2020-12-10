from contextlib import closing
from db_core import DB_core
from models import Pulse

class DAL_pulse:

    @classmethod
    def add_pulse(cls, pulse):
        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
                INSERT INTO pulse 
                    (userId, pulse, activity, notes, recordDateTime )
                VALUES
                    (?, ?, ?, ?, ?, ?)""", (pulse.userId, pulse.pulse, pulse.activity, pulse.notes, pulse.recordDateTime,))
            con.commit()
        return pulse    